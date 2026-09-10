# CareBridge Sample Data Generator
#
# This script populates the CareBridge database with realistic test data.
# Run this ONCE after creating your database and tables (schema.sql).
# Running it twice will cause errors because some unique values will repeat.

# Required libraries. Install them before running this script:
#   pip install mysql-connector-python
#   pip install Faker
#   pip install python-dotenv

import os
import mysql.connector
import random
from faker import Faker
from datetime import date, timedelta, datetime
import decimal
from dotenv import load_dotenv

load_dotenv()

# Create a Faker instance set to India so names look realistic.
fake = Faker('en_IN')

# ─── DATABASE CONNECTION ────────────────────────────────────────────────────
# Database credentials are loaded from the .env file.
connection = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'CareBridge')
)

cursor = connection.cursor()

print('Connected to MySQL successfully.')
# ─── CONSTANTS ──────────────────────────────────────────────────────────────
NUM_DOCTORS      = 40
NUM_PATIENTS     = 500
NUM_APPOINTMENTS = 3000
NUM_BILLS        = 2500
BILL_REJECT_LOW  = 0.08   # 8 percent minimum rejection rate
BILL_REJECT_HIGH = 0.12   # 12 percent maximum rejection rate
PRESCRIPTION_RATE = 0.55  # fraction of completed appointments that get a prescription

DEPARTMENTS = [
    'Cardiology', 'General Medicine', 'Orthopaedics', 'Gynaecology',
    'Paediatrics', 'Neurology', 'Dermatology', 'Ophthalmology',
    'ENT', 'Psychiatry', 'Oncology', 'Urology', 'Endocrinology'
]

QUALIFICATIONS = [
    'MBBS, MD', 'MBBS, MS', 'MD Cardiology', 'MS Orthopaedics',
    'MD Paediatrics', 'MD Dermatology', 'DM Neurology', 'MS Gynaecology',
    'MS ENT', 'MD Psychiatry'
]

WORKING_DAYS_OPTIONS = [
    'Mon,Tue,Wed,Thu,Fri', 'Mon,Wed,Fri', 'Tue,Thu,Sat',
    'Mon,Tue,Wed,Thu,Fri,Sat', 'Mon,Wed,Thu,Fri'
]

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']

INSURERS = ['Star Health', 'HDFC Ergo', 'ICICI Lombard', 'Bajaj Allianz', 'Care Health', None, None]

DIAGNOSES = [
    'Hypertension', 'Type 2 Diabetes', 'Upper Respiratory Infection',
    'Migraine', 'Lumbar Spondylosis', 'Anxiety Disorder', 'Anaemia',
    'Hypothyroidism', 'Gastritis', 'Urinary Tract Infection',
    'Dengue Fever', 'Viral Fever', 'Asthma', 'Arthritis', 'Obesity',
    'Iron Deficiency', 'Vitamin D Deficiency', 'Sinusitis', 'Eczema'
]

CONSULT_MODES = ['In-Person', 'In-Person', 'In-Person', 'Video', 'Home Visit']

ALLERGIES = ['Pollen, dust', 'Penicillin', 'Peanuts', 'Dust mites', 'Latex']

MEDICINES = [
    ('Atenolol', '25mg'), ('Cetirizine', '10mg'), ('Ibuprofen', '400mg'),
    ('Ferrous Sulphate', '325mg'), ('Amoxicillin', '500mg'), ('Metformin', '500mg'),
    ('Paracetamol', '650mg'), ('Azithromycin', '500mg'), ('Losartan', '50mg'),
    ('Omeprazole', '20mg')
]

DURATIONS = ['3 days', '5 days', '7 days', '10 days', '14 days', '30 days', '60 days', '90 days']

INSTRUCTIONS = [
    'Once daily after breakfast', 'Twice daily after food', 'Once daily at night',
    'Three times daily', 'Once daily with vitamin C', 'Twice daily before meals'
]

REJECTION_REASONS = [
    'Insurance claim limit exceeded for this policy year.',
    'Procedure not covered under current insurance plan.',
    'Pre-authorisation was not obtained before treatment.',
    'Patient not eligible under submitted insurance policy number.',
    'Duplicate claim submitted for the same service date.',
    'Medical documents submitted are incomplete.',
    'Claim submitted after the deadline specified by insurer.'
]

# ─── STEP 1: INSERT DOCTORS ─────────────────────────────────────────────────
print(f'Inserting {NUM_DOCTORS} doctors...')

doctor_ids = []  # We store the IDs so we can use them for appointments later.

for i in range(NUM_DOCTORS):
    name        = 'Dr. ' + fake.name()
    department  = random.choice(DEPARTMENTS)
    spec        = department
    qualification = random.choice(QUALIFICATIONS)
    experience  = random.randint(2, 25)
    phone       = '9' + str(random.randint(100000000, 999999999))
    email       = f'doctor{i+1}@carebridge.in'
    address     = fake.city() + ', Maharashtra'
    lic         = f'MCI-{2000 + i:04d}'
    working_days = random.choice(WORKING_DAYS_OPTIONS)
    joining_date = fake.date_between(start_date='-15y', end_date='-1y')
    is_active   = 1 if random.random() > 0.05 else 0

    cursor.execute(
        '''
        INSERT INTO doctor
            (full_name, department, specialisation, qualification, experience_years,
             phone, email, address, licence_number, working_days, joining_date, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (name, department, spec, qualification, experience,
         phone, email, address, lic, working_days, joining_date, is_active)
    )
    doctor_ids.append(cursor.lastrowid)

connection.commit()
print(f'  Done. Inserted {len(doctor_ids)} doctors.')

# ─── STEP 2: INSERT DIGITAL CONSULTANT (one row per doctor) ────────────────
print('Inserting digital_consultant rows (one per doctor)...')

for d_id in doctor_ids:
    home_visit  = random.choice(['Yes', 'No'])
    video       = random.choice(['Yes', 'Yes', 'No'])
    emergency   = random.choice(['Yes', 'No', 'No'])
    on_leave    = 1 if random.random() < 0.1 else 0
    avail_today = 0 if on_leave else (1 if random.random() > 0.15 else 0)
    slots_today = random.randint(2, 10) if avail_today else 0
    verified    = 1 if random.random() > 0.1 else 0

    cursor.execute(
        '''
        INSERT INTO digital_consultant
            (doctor_id, home_visit_available, video_consult_available, emergency_available,
             available_today, available_slots_today, on_leave, is_verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (d_id, home_visit, video, emergency, avail_today, slots_today, on_leave, verified)
    )

connection.commit()
print(f'  Done. Inserted {len(doctor_ids)} digital_consultant rows.')

# ─── STEP 3: INSERT PATIENTS ────────────────────────────────────────────────
print(f'Inserting {NUM_PATIENTS} patients...')

patient_ids = []

for i in range(NUM_PATIENTS):
    name      = fake.name()
    dob       = fake.date_of_birth(minimum_age=5, maximum_age=85)
    gender    = random.choice(['Male', 'Female', 'Other'])
    phone     = '9' + str(random.randint(100000000, 999999999))
    email     = f'patient{i+1}@example.com'
    address   = fake.address().replace('\n', ', ')
    blood     = random.choice(BLOOD_GROUPS)
    ec_name   = fake.name()
    ec_phone  = '9' + str(random.randint(100000000, 999999999))

    insurer   = random.choice(INSURERS)
    policy_no = f'POL-{5000 + i}' if insurer else None

    ai_summary = random.choice([
        'Routine checkups, no major history.',
        'History of seasonal allergies.',
        'Post-surgery follow-up patient.',
        'New patient, first visit.',
        'Regular diabetic checkups.',
        'History of hypertension, on medication.',
        'No significant medical history recorded.'
    ])

    home_visit_requested = 1 if random.random() < 0.1 else 0
    follow_up_required   = 1 if random.random() < 0.25 else 0
    is_admitted           = 1 if random.random() < 0.08 else 0
    is_critical            = 1 if (is_admitted and random.random() < 0.3) else 0
    has_allergies           = 1 if random.random() < 0.15 else 0
    allergy_details          = random.choice(ALLERGIES) if has_allergies else None

    cursor.execute(
        '''
        INSERT INTO patient
            (full_name, date_of_birth, gender, phone, email, address,
             blood_group, emergency_contact_name, emergency_contact_phone,
             insurance_provider, insurance_policy_no, ai_summary,
             home_visit_requested, follow_up_required, is_admitted,
             is_critical, has_allergies, allergy_details)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (name, dob, gender, phone, email, address, blood, ec_name, ec_phone,
         insurer, policy_no, ai_summary, home_visit_requested, follow_up_required,
         is_admitted, is_critical, has_allergies, allergy_details)
    )
    patient_ids.append(cursor.lastrowid)

connection.commit()
print(f'  Done. Inserted {len(patient_ids)} patients.')

# ─── STEP 4: INSERT APPOINTMENTS ────────────────────────────────────────────
print(f'Inserting {NUM_APPOINTMENTS} appointments...')

appointment_ids = []
completed_appointment_ids = []  # track which ones are Completed, for billing/prescriptions

start_date = date.today() - timedelta(days=730)
end_date   = date.today()

hour_options   = list(range(9, 17))
minute_options = [0, 15, 30, 45]

for _ in range(NUM_APPOINTMENTS):
    p_id    = random.choice(patient_ids)
    d_id    = random.choice(doctor_ids)
    appt_dt = start_date + timedelta(days=random.randint(0, 730))
    appt_tm = f'{random.choice(hour_options):02d}:{random.choice(minute_options):02d}:00'
    mode    = random.choice(CONSULT_MODES)
    reason  = 'Patient complaints of ' + random.choice(DIAGNOSES).lower()

    status  = random.choices(
        ['Completed', 'Scheduled', 'Cancelled'],
        weights=[80, 10, 10]
    )[0]

    if status == 'Completed':
        diagnosis = random.choice(DIAGNOSES)
        notes = random.choice([
            'Advised follow-up in 2 weeks', 'No concerns', 'Prescribed medication',
            'Physiotherapy advised', 'Continue current medication', None
        ])
        report_summary = random.choice([
            'All vitals normal', 'Blood test pending', 'Mobility improving',
            'Under monitoring', 'Sugar levels stable', None
        ])
    else:
        diagnosis = None
        notes = None
        report_summary = None

    cursor.execute(
        '''
        INSERT INTO appointment
            (patient_id, doctor_id, appointment_date, appointment_time, consult_mode,
             reason, diagnosis, notes, report_summary, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (p_id, d_id, appt_dt, appt_tm, mode, reason, diagnosis, notes, report_summary, status)
    )
    new_id = cursor.lastrowid
    appointment_ids.append(new_id)
    if status == 'Completed':
        completed_appointment_ids.append((new_id, p_id))

connection.commit()
print(f'  Done. Inserted {len(appointment_ids)} appointments.')
print(f'  ({len(completed_appointment_ids)} of them are Completed.)')

# ─── STEP 5: INSERT PRESCRIPTIONS ───────────────────────────────────────────
print('Inserting prescriptions for completed appointments...')

presc_targets = random.sample(
    completed_appointment_ids,
    k=int(len(completed_appointment_ids) * PRESCRIPTION_RATE)
)

prescriptions_inserted = 0
for (appt_id, _p_id) in presc_targets:
    medicine, dosage = random.choice(MEDICINES)
    duration = random.choice(DURATIONS)
    instructions = random.choice(INSTRUCTIONS)

    cursor.execute(
        '''
        INSERT INTO prescription (appointment_id, medicine_name, dosage, duration, instructions)
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (appt_id, medicine, dosage, duration, instructions)
    )
    prescriptions_inserted += 1

connection.commit()
print(f'  Done. Inserted {prescriptions_inserted} prescriptions.')

# ─── STEP 6: INSERT BILLS ───────────────────────────────────────────────────
print(f'Inserting up to {NUM_BILLS} bills...')

if len(completed_appointment_ids) < NUM_BILLS:
    print(f'  Note: Only {len(completed_appointment_ids)} completed appointments available.')
    print(f'  Will create one bill per completed appointment instead of {NUM_BILLS}.')
    bills_to_create = completed_appointment_ids
else:
    bills_to_create = random.sample(completed_appointment_ids, NUM_BILLS)

reject_rate = random.uniform(BILL_REJECT_LOW, BILL_REJECT_HIGH)
print(f'  Bill rejection rate for this run: {reject_rate*100:.1f}%')

bills_inserted = 0

for (appt_id, p_id) in bills_to_create:
    total = round(random.uniform(300, 6000), 2)
    rand_val = random.random()

    # decide insurance claim details first
    has_claim = random.random() > 0.4
    if has_claim:
        claim_number   = f'CLM-{6000 + bills_inserted}'
        insurance_provider = random.choice(
            ['Star Health', 'HDFC Ergo', 'ICICI Lombard', 'Bajaj Allianz', 'Care Health']
        )
        total_claim_amount = round(total * random.uniform(0.6, 1.0), 2)
    else:
        claim_number = None
        insurance_provider = None
        total_claim_amount = 0.00

    if rand_val < reject_rate:
        status         = 'Rejected'
        claim_status   = 'Rejected' if has_claim else 'Pending'
        amount_paid    = 0.00
        discount       = 0.00
        refund_amount  = 0.00
        total_insurance_amount = 0.00
        reject_reason  = random.choice(REJECTION_REASONS)

    elif rand_val < reject_rate + 0.10:
        status         = 'Partially Paid'
        claim_status   = 'Pending' if has_claim else 'Pending'
        paid_pct       = random.uniform(0.30, 0.70)
        amount_paid    = round(total * paid_pct, 2)
        discount       = 0.00
        refund_amount  = 0.00
        total_insurance_amount = 0.00
        reject_reason  = None

    elif rand_val < reject_rate + 0.15:
        status         = 'Pending'
        claim_status   = 'Pending'
        amount_paid    = 0.00
        discount       = 0.00
        refund_amount  = 0.00
        total_insurance_amount = 0.00
        reject_reason  = None

    elif rand_val < reject_rate + 0.18:
        status         = 'Payment Failed'
        claim_status   = 'Rejected' if has_claim else 'Pending'
        amount_paid    = 0.00
        discount       = 0.00
        refund_amount  = 0.00
        total_insurance_amount = 0.00
        reject_reason  = random.choice(REJECTION_REASONS)

    else:
        status         = 'Paid'
        claim_status   = 'Accepted' if has_claim else 'Pending'
        discount       = round(total * random.uniform(0, 0.05), 2)
        amount_paid    = round(total - discount, 2)
        refund_amount  = 0.00
        total_insurance_amount = round(total_claim_amount * random.uniform(0.5, 1.0), 2) if has_claim else 0.00
        reject_reason  = None

    invoice_number = f'INV-{7000 + bills_inserted}'
    ai_summary = random.choice([
        'Claim processed and approved.', 'Claim under review by insurer.',
        'Self-pay, no insurance claim filed.', 'Claim rejected, missing documents.',
        'Partial payment received, balance pending.'
    ])

    cursor.execute(
        'SELECT appointment_date FROM appointment WHERE appointment_id = %s',
        (appt_id,)
    )
    row = cursor.fetchone()
    appt_date = row[0]
    bill_date = appt_date + timedelta(days=random.randint(0, 2))
    due_date  = bill_date + timedelta(days=30)

    cursor.execute(
        '''
        INSERT INTO billing
            (appointment_id, patient_id, total_amount, amount_paid, discount, refund_amount,
             claim_number, insurance_provider, total_claim_amount, total_insurance_amount,
             claim_status, invoice_number, ai_summary, status, rejection_reason,
             bill_date, due_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (appt_id, p_id, total, amount_paid, discount, refund_amount,
         claim_number, insurance_provider, total_claim_amount, total_insurance_amount,
         claim_status, invoice_number, ai_summary, status, reject_reason,
         bill_date, due_date)
    )
    bills_inserted += 1

connection.commit()
print(f'  Done. Inserted {bills_inserted} bills.')

# ─── STEP 7: INSERT ACTIVITY LOG ────────────────────────────────────────────
NUM_LOGS = 300
print(f'Inserting {NUM_LOGS} activity_log rows...')

actions = ['CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'VIEW']
targets = ['appointment', 'patient', 'billing', 'prescription', 'doctor']
user_types = ['Doctor', 'Patient']

for _ in range(NUM_LOGS):
    user_type = random.choice(user_types)
    user_id   = random.choice(doctor_ids) if user_type == 'Doctor' else random.choice(patient_ids)
    action    = random.choice(actions)
    target    = random.choice(targets)
    target_id = random.choice(appointment_ids)
    old_value = None if action == 'CREATE' else 'previous value'
    new_value = 'updated value' if action in ('UPDATE', 'CREATE') else None
    ip = fake.ipv4()

    cursor.execute(
        '''
        INSERT INTO activity_log
            (user_type, user_id, action, target_table, target_id, old_value, new_value, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (user_type, user_id, action, target, target_id, old_value, new_value, ip)
    )

connection.commit()
print('  Done.')

# ─── STEP 8: VERIFY ROW COUNTS ──────────────────────────────────────────────
print()
print('=== FINAL ROW COUNTS ===')

for table in ['doctor', 'digital_consultant', 'patient', 'appointment',
              'prescription', 'billing', 'activity_log']:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f'  {table:20s}: {count} rows')

# ─── CLEANUP ────────────────────────────────────────────────────────────────
cursor.close()
connection.close()
print()
print('Done. CareBridge database is ready for use.')