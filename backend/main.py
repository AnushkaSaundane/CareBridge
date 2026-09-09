# main.py
# CareBridge Patient Portal Backend
#
# This file is a FastAPI application.
# It connects to the MySQL database (carebridge) and provides API endpoints.
# The Vue.js frontend will call these endpoints to get data.
#
# To run this file:
#   python -m uvicorn main:app --reload

from fastapi import FastAPI, HTTPException           # the web framework
from fastapi.middleware.cors import CORSMiddleware   # allows browser to call this API
import mysql.connector                                # connects to MySQL
import config                                          # your database settings file

# ── Create the FastAPI application ──────────────────────────────────────────
app = FastAPI(title='CareBridge API')

# ── CORS Configuration ───────────────────────────────────────────────────────
# CORS stands for Cross-Origin Resource Sharing.
# Without this, the browser will block the Vue.js dashboard from calling this API.
# allow_origins=['*'] means: accept requests from any browser tab.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET'],
    allow_headers=['*'],
)

# ── Database connection helper ───────────────────────────────────────────────
# This function creates a fresh connection to MySQL every time it is called.
# Settings come from config.py so the password is not hardcoded here.
def get_db():
    return mysql.connector.connect(
        host=config.DATABASE_HOST,
        port=config.DATABASE_PORT,
        user=config.DATABASE_USER,
        password=config.DATABASE_PASSWORD,
        database=config.DATABASE_NAME
    )

# ── Basic health check ───────────────────────────────────────────────────────
# URL: http://127.0.0.1:8000/
@app.get('/')
def read_root():
    return {'message': 'CareBridge API is running'}

# ── ENDPOINT: Summary numbers ────────────────────────────────────────────────
# URL: http://127.0.0.1:8000/summary
# Returns: total counts for patients, doctors, appointments, and bills
@app.get('/summary')
def get_summary():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Count patients that haven't been soft-deleted
    cursor.execute('SELECT COUNT(*) AS total FROM patient WHERE is_deleted = 0')
    patients = cursor.fetchone()['total']

    # Count active doctors only
    cursor.execute('SELECT COUNT(*) AS total FROM doctor WHERE is_active = 1')
    doctors = cursor.fetchone()['total']

    # Count all appointments
    cursor.execute('SELECT COUNT(*) AS total FROM appointment')
    appointments = cursor.fetchone()['total']

    # Count all bills
    cursor.execute('SELECT COUNT(*) AS total FROM billing')
    bills = cursor.fetchone()['total']

    # Count rejected bills
    cursor.execute("SELECT COUNT(*) AS total FROM billing WHERE status = 'Rejected'")
    rejected = cursor.fetchone()['total']

    rejection_rate = round((rejected / bills * 100), 1) if bills > 0 else 0

    # Total revenue collected so far
    cursor.execute('SELECT ROUND(SUM(amount_paid), 2) AS total FROM billing')
    revenue = cursor.fetchone()['total'] or 0

    cursor.close()
    db.close()

    return {
        'total_patients':     patients,
        'total_doctors':      doctors,
        'total_appointments': appointments,
        'total_bills':        bills,
        'rejection_rate':     rejection_rate,
        'total_revenue':      float(revenue),
    }

# ── ENDPOINT: Patient list ───────────────────────────────────────────────────
# URL: http://127.0.0.1:8000/patients
# Returns: list of 50 most recently registered active patients
@app.get('/patients')
def get_patients():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
            patient_id,
            full_name,
            gender,
            blood_group,
            DATE_FORMAT(date_of_birth, '%d %b %Y') AS date_of_birth,
            DATE_FORMAT(created_at,    '%d %b %Y') AS registered_on
        FROM patient
        WHERE is_deleted = 0
        ORDER BY created_at DESC
        LIMIT 50
        '''
    )
    patients = cursor.fetchall()

    cursor.close()
    db.close()

    return {'patients': patients}

# ── ENDPOINT: Single patient by ID (Milestone 6) ─────────────────────────────
# URL: http://127.0.0.1:8000/patients/{patient_id}
# Returns: one patient's full details, or 404 if not found
@app.get('/patients/{patient_id}')
def get_patient(patient_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
            patient_id,
            full_name,
            gender,
            blood_group,
            phone,
            email,
            DATE_FORMAT(date_of_birth, '%d %b %Y') AS date_of_birth
        FROM patient
        WHERE patient_id = %s AND is_deleted = 0
        ''',
        (patient_id,)
    )
    patient = cursor.fetchone()

    cursor.close()
    db.close()

    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')

    return patient

# ── ENDPOINT: Appointments for a patient (Milestone 7) ───────────────────────
# URL: http://127.0.0.1:8000/patients/{patient_id}/appointments
# Returns: list of appointments for that patient (empty list if none)
@app.get('/patients/{patient_id}/appointments')
def get_patient_appointments(patient_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
            a.appointment_id,
            a.appointment_date,
            a.appointment_time,
            a.consult_mode,
            a.status,
            d.full_name AS doctor_name
        FROM appointment a
        JOIN doctor d ON d.doctor_id = a.doctor_id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_date DESC
        ''',
        (patient_id,)
    )
    appointments = cursor.fetchall()

    cursor.close()
    db.close()

    return appointments

# ── ENDPOINT: Billing summary ────────────────────────────────────────────────
# URL: http://127.0.0.1:8000/billing
# Returns: recent 50 bills with patient name and status
@app.get('/billing')
def get_billing():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
            b.bill_id,
            p.full_name AS patient_name,
            b.total_amount,
            b.amount_paid,
            b.status,
            DATE_FORMAT(b.bill_date, '%d %b %Y') AS bill_date
        FROM billing b
        JOIN patient p ON p.patient_id = b.patient_id
        ORDER BY b.created_at DESC
        LIMIT 50
        '''
    )
    bills = cursor.fetchall()

    # Convert Decimal types to float so JSON serialisation works correctly
    for bill in bills:
        bill['total_amount'] = float(bill['total_amount'])
        bill['amount_paid'] = float(bill['amount_paid'])

    cursor.close()
    db.close()

    return {'bills': bills}

# ── ENDPOINT: Doctor list with appointment counts ────────────────────────────
# URL: http://127.0.0.1:8000/doctors
# Returns: all active doctors with their completed appointment count
@app.get('/doctors')
def get_doctors():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
            d.doctor_id,
            d.full_name,
            d.specialisation,
            COUNT(a.appointment_id) AS total_appointments
        FROM doctor d
        LEFT JOIN appointment a ON a.doctor_id = d.doctor_id
            AND a.status = 'Completed'
        WHERE d.is_active = 1
        GROUP BY d.doctor_id, d.full_name, d.specialisation
        ORDER BY total_appointments DESC
        '''
    )
    doctors = cursor.fetchall()

    cursor.close()
    db.close()

    return {'doctors': doctors}

# ── ENDPOINT: Doctor appointment summary from view (Milestone 11) ───────────
# URL: http://127.0.0.1:8000/analytics/doctors
# Returns: data from vw_doctor_appointment_summary (Milestone 9/10 view)
@app.get('/analytics/doctors')
def get_doctor_analytics():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('SELECT * FROM vw_doctor_appointment_summary')
    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results

@app.get('/analytics/heatmap')
def get_appointment_heatmap():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            DATE_FORMAT(appointment_date, '%a') AS day,
            COUNT(*) AS appointments,
            DAYOFWEEK(appointment_date) AS day_number
        FROM appointment
        GROUP BY
            DAYOFWEEK(appointment_date),
            DATE_FORMAT(appointment_date, '%a')
        ORDER BY day_number
    """)

    results = cursor.fetchall()

    cursor.close()
    db.close()

    # Remove helper column before sending data to frontend
    for row in results:
        row.pop("day_number", None)

    return results

# ── ENDPOINT: Revenue trend ─────────────────────────────────────────────────
# URL: http://127.0.0.1:8000/analytics/revenue
# Returns: total revenue collected for each month

@app.get('/analytics/revenue')
def get_revenue_analytics():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
            DATE_FORMAT(bill_date, '%Y-%m') AS month,
            ROUND(SUM(amount_paid), 2) AS revenue
        FROM billing
        GROUP BY DATE_FORMAT(bill_date, '%Y-%m')
        ORDER BY month
        '''
    )

    results = cursor.fetchall()

    # Convert Decimal to float for JSON
    for row in results:
        row['revenue'] = float(row['revenue'] or 0)

    cursor.close()
    db.close()

    return results


# ── ENDPOINT: Blood group distribution ──────────────────────────────────────
# URL: http://127.0.0.1:8000/analytics/blood-group
# Returns: number of patients in each blood group

@app.get('/analytics/blood-group')
def get_blood_group_analytics():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
            blood_group,
            COUNT(*) AS count
        FROM patient
        WHERE is_deleted = 0
        GROUP BY blood_group
        ORDER BY blood_group
        '''
    )

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results