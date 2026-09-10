# read_data.py
# CareBridge Database Reader
#
# This script demonstrates how to connect Python to MySQL
# and run queries to extract meaningful information.
# This pattern is the foundation of every backend API you will build.

import os
import mysql.connector
from dotenv import load_dotenv
from datetime import date

# Load database credentials from .env
load_dotenv()

# ─── DATABASE CONNECTION ────────────────────────────────────────────────────
# Database credentials are loaded from environment variables.
connection = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'carebridge')
)

cursor = connection.cursor(dictionary=True)

print('Connected to CareBridge database.')
print('=' * 60)

# ─── QUERY 1: How many doctors in each specialisation? ──────────────────────
print()
print('QUERY 1: Doctor Count by Specialisation')
print('-' * 45)

cursor.execute(
    '''
    SELECT
        specialisation,
        COUNT(*) AS total_doctors
    FROM doctor
    WHERE is_active = 1
    GROUP BY specialisation
    ORDER BY total_doctors DESC
    '''
)

rows = cursor.fetchall()
for row in rows:
    print(f"  {row['specialisation']:<25} {row['total_doctors']} doctors")

print()

# ─── QUERY 2: Total revenue by billing status ───────────────────────────────
print('QUERY 2: Revenue Summary by Bill Status')
print('-' * 45)

cursor.execute(
    '''
    SELECT
        status,
        COUNT(*)                        AS total_bills,
        ROUND(SUM(total_amount), 2)     AS total_billed,
        ROUND(SUM(amount_paid), 2)      AS total_collected,
        ROUND(AVG(total_amount), 2)     AS avg_bill_amount
    FROM billing
    GROUP BY status
    ORDER BY total_billed DESC
    '''
)

rows = cursor.fetchall()
for row in rows:
    print(f"  {row['status']:<15}  Bills: {row['total_bills']:>5}  "
          f"Billed: Rs {row['total_billed']:>10}  "
          f"Collected: Rs {row['total_collected']:>10}")

print()

# ─── QUERY 3: Rejection rate calculation ────────────────────────────────────
print('QUERY 3: Bill Rejection Rate')
print('-' * 45)

cursor.execute('SELECT COUNT(*) AS total FROM billing')
total_bills = cursor.fetchone()['total']

cursor.execute("SELECT COUNT(*) AS rejected FROM billing WHERE status = 'Rejected'")
rejected_bills = cursor.fetchone()['rejected']

rejection_rate = (rejected_bills / total_bills * 100) if total_bills > 0 else 0
print(f'  Total Bills    : {total_bills}')
print(f'  Rejected Bills : {rejected_bills}')
print(f'  Rejection Rate : {rejection_rate:.2f}%')

print()

# ─── QUERY 4: Top 5 busiest doctors ─────────────────────────────────────────
print('QUERY 4: Top 5 Busiest Doctors by Appointments')
print('-' * 50)

cursor.execute(
    '''
    SELECT
        d.full_name,
        d.specialisation,
        COUNT(a.appointment_id) AS total_appointments
    FROM doctor d
    JOIN appointment a ON a.doctor_id = d.doctor_id
    WHERE a.status = 'Completed'
    GROUP BY d.doctor_id, d.full_name, d.specialisation
    ORDER BY total_appointments DESC
    LIMIT 5
    '''
)

rows = cursor.fetchall()
for i, row in enumerate(rows, start=1):
    print(f"  {i}. {row['full_name']:<30} ({row['specialisation']:<20})"
          f"  {row['total_appointments']} completed appointments")

print()

# ─── QUERY 5: Patients with more than 5 visits ──────────────────────────────
print('QUERY 5: Patients With More Than 5 Completed Visits')
print('-' * 52)

cursor.execute(
    '''
    SELECT
        p.full_name,
        p.blood_group,
        COUNT(a.appointment_id) AS visit_count
    FROM patient p
    JOIN appointment a ON a.patient_id = p.patient_id
    WHERE a.status = 'Completed'
      AND p.is_deleted = 0
    GROUP BY p.patient_id, p.full_name, p.blood_group
    HAVING visit_count > 5
    ORDER BY visit_count DESC
    LIMIT 10
    '''
)

rows = cursor.fetchall()
if not rows:
    print('  No patients with more than 5 visits found.')
else:
    for row in rows:
        print(f"  {row['full_name']:<30} Blood: {row['blood_group']:<4}"
              f"  Visits: {row['visit_count']}")

print()

# ─── QUERY 6: Monthly appointment trend (last 6 months) ─────────────────────
print('QUERY 6: Monthly Appointment Count (Last 6 Months)')
print('-' * 52)

cursor.execute(
    '''
    SELECT
        DATE_FORMAT(appointment_date, '%Y-%m') AS month,
        COUNT(*)                               AS total_appointments
    FROM appointment
    WHERE appointment_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
    GROUP BY month
    ORDER BY month ASC
    '''
)

rows = cursor.fetchall()
for row in rows:
    print(f"  {row['month']}   {row['total_appointments']} appointments")

print()

# ─── QUERY 7 (NEW): Doctors available for digital consult today ────────────
print('QUERY 7: Doctors Available for Digital Consult Today')
print('-' * 54)

cursor.execute(
    '''
    SELECT
        d.full_name,
        d.specialisation,
        dc.video_consult_available,
        dc.home_visit_available,
        dc.available_slots_today
    FROM digital_consultant dc
    JOIN doctor d ON d.doctor_id = dc.doctor_id
    WHERE dc.available_today = 1
      AND dc.on_leave = 0
    ORDER BY dc.available_slots_today DESC
    '''
)

rows = cursor.fetchall()
if not rows:
    print('  No doctors currently marked available today.')
else:
    for row in rows:
        print(f"  {row['full_name']:<30} ({row['specialisation']:<15})  "
              f"Video: {row['video_consult_available']:<3}  "
              f"Home Visit: {row['home_visit_available']:<3}  "
              f"Slots: {row['available_slots_today']}")

print()

# ─── QUERY 8 (NEW): Most prescribed medicines ───────────────────────────────
print('QUERY 8: Top 5 Most Prescribed Medicines')
print('-' * 45)

cursor.execute(
    '''
    SELECT
        medicine_name,
        COUNT(*) AS times_prescribed
    FROM prescription
    GROUP BY medicine_name
    ORDER BY times_prescribed DESC
    LIMIT 5
    '''
)

rows = cursor.fetchall()
for row in rows:
    print(f"  {row['medicine_name']:<20} {row['times_prescribed']} prescriptions")

print()

# ─── QUERY 9 (NEW): Insurance claim outcomes ────────────────────────────────
print('QUERY 9: Insurance Claim Outcomes')
print('-' * 45)

cursor.execute(
    '''
    SELECT
        claim_status,
        COUNT(*)                          AS total_claims,
        ROUND(SUM(total_claim_amount), 2) AS total_claimed,
        ROUND(SUM(total_insurance_amount), 2) AS total_paid_by_insurer
    FROM billing
    WHERE claim_number IS NOT NULL
    GROUP BY claim_status
    ORDER BY total_claims DESC
    '''
)

rows = cursor.fetchall()
for row in rows:
    print(f"  {row['claim_status']:<12}  Claims: {row['total_claims']:>5}  "
          f"Claimed: Rs {row['total_claimed']:>10}  "
          f"Paid by insurer: Rs {row['total_paid_by_insurer']:>10}")

print()
print('=' * 60)
print('All queries completed successfully.')

# ─── CLEANUP ────────────────────────────────────────────────────────────────
cursor.close()
connection.close()