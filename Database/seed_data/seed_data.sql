- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- CareBridge Seed Data
-- Run AFTER carebridge_schema_v2.sql
-- =============================================================
USE carebridge;

-- -------------------------------------------------------------
-- doctor
-- -------------------------------------------------------------
INSERT INTO
    doctor (
        full_name,
        department,
        specialisation,
        qualification,
        experience_years,
        phone,
        email,
        address,
        licence_number,
        working_days,
        joining_date,
        is_active
    )
VALUES
    (
        'Dr. Anjali Deshmukh',
        'Cardiology',
        'Cardiologist',
        'MD Cardiology',
        12,
        '9876543210',
        'anjali.deshmukh@carebridge.com',
        'Pune, MH',
        'LIC-1001',
        'Mon,Tue,Wed,Thu,Fri',
        '2015-06-01',
        1
    ),
    (
        'Dr. Rohan Patil',
        'Orthopedics',
        'Orthopedic Surgeon',
        'MS Ortho',
        9,
        '9876543211',
        'rohan.patil@carebridge.com',
        'Pune, MH',
        'LIC-1002',
        'Mon,Wed,Fri',
        '2017-03-15',
        1
    ),
    (
        'Dr. Sneha Kulkarni',
        'Pediatrics',
        'Pediatrician',
        'MD Pediatrics',
        7,
        '9876543212',
        'sneha.kulkarni@carebridge.com',
        'Pimpri, MH',
        'LIC-1003',
        'Tue,Thu,Sat',
        '2019-01-10',
        1
    ),
    (
        'Dr. Vikram Joshi',
        'General Medicine',
        'General Physician',
        'MBBS, MD',
        15,
        '9876543213',
        'vikram.joshi@carebridge.com',
        'Pune, MH',
        'LIC-1004',
        'Mon,Tue,Wed,Thu,Fri,Sat',
        '2010-08-20',
        1
    ),
    (
        'Dr. Priya Nair',
        'Dermatology',
        'Dermatologist',
        'MD Dermatology',
        6,
        '9876543214',
        'priya.nair@carebridge.com',
        'Pune, MH',
        'LIC-1005',
        'Mon,Tue,Thu',
        '2020-02-01',
        1
    );

-- -------------------------------------------------------------
-- digital_consultant (one row per doctor)
-- -------------------------------------------------------------
INSERT INTO
    digital_consultant (
        doctor_id,
        home_visit_available,
        video_consult_available,
        emergency_available,
        available_today,
        available_slots_today,
        on_leave,
        is_verified
    )
VALUES
    (1, 'Yes', 'Yes', 'No', 1, 4, 0, 1),
    (2, 'No', 'Yes', 'No', 1, 2, 0, 1),
    (3, 'Yes', 'Yes', 'Yes', 0, 0, 1, 1),
    (4, 'Yes', 'No', 'Yes', 1, 6, 0, 1),
    (5, 'No', 'Yes', 'No', 1, 3, 0, 0);

-- -------------------------------------------------------------
-- patient
-- -------------------------------------------------------------
INSERT INTO
    patient (
        full_name,
        date_of_birth,
        gender,
        phone,
        email,
        address,
        blood_group,
        emergency_contact_name,
        emergency_contact_phone,
        insurance_provider,
        insurance_policy_no,
        ai_summary,
        home_visit_requested,
        follow_up_required,
        is_admitted,
        is_critical,
        has_allergies,
        allergy_details
    )
VALUES
    (
        'Aditya Sharma',
        '1990-05-14',
        'Male',
        '9000000001',
        'aditya.sharma@mail.com',
        'Pune, MH',
        'B+',
        'Rekha Sharma',
        '9000000101',
        'Star Health',
        'POL-2001',
        'Routine checkups, no major history.',
        0,
        0,
        0,
        0,
        0,
        NULL
    ),
    (
        'Neha Verma',
        '1985-11-02',
        'Female',
        '9000000002',
        'neha.verma@mail.com',
        'Pimpri, MH',
        'O+',
        'Suresh Verma',
        '9000000102',
        'HDFC Ergo',
        'POL-2002',
        'History of seasonal allergies.',
        0,
        1,
        0,
        0,
        1,
        'Pollen, dust'
    ),
    (
        'Karan Mehta',
        '1978-02-20',
        'Male',
        '9000000003',
        'karan.mehta@mail.com',
        'Chinchwad, MH',
        'A-',
        'Priya Mehta',
        '9000000103',
        'ICICI Lombard',
        'POL-2003',
        'Post-surgery follow-up patient.',
        0,
        1,
        1,
        0,
        0,
        NULL
    ),
    (
        'Ishita Rao',
        '2001-07-09',
        'Female',
        '9000000004',
        'ishita.rao@mail.com',
        'Pune, MH',
        'AB+',
        'Manoj Rao',
        '9000000104',
        NULL,
        NULL,
        'New patient, first visit.',
        1,
        0,
        0,
        0,
        0,
        NULL
    ),
    (
        'Farhan Sheikh',
        '1995-09-30',
        'Male',
        '9000000005',
        'farhan.sheikh@mail.com',
        'Pune, MH',
        'O-',
        'Ayesha Sheikh',
        '9000000105',
        'Star Health',
        'POL-2005',
        'Admitted for observation.',
        0,
        0,
        1,
        1,
        0,
        NULL
    ),
    (
        'Pooja Iyer',
        '1992-12-18',
        'Female',
        '9000000006',
        'pooja.iyer@mail.com',
        'Pimpri, MH',
        'B-',
        'Ramesh Iyer',
        '9000000106',
        'HDFC Ergo',
        'POL-2006',
        'Regular diabetic checkups.',
        0,
        1,
        0,
        0,
        0,
        NULL
    );

-- -------------------------------------------------------------
-- appointment
-- -------------------------------------------------------------
INSERT INTO
    appointment (
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        consult_mode,
        reason,
        diagnosis,
        notes,
        report_summary,
        status
    )
VALUES
    (
        1,
        1,
        '2026-08-01',
        '10:00:00',
        'In-Person',
        'Chest discomfort',
        'Mild arrhythmia',
        'Advised ECG follow-up',
        'ECG normal range',
        'Completed'
    ),
    (
        1,
        4,
        '2026-08-15',
        '11:30:00',
        'Video',
        'General checkup',
        'Healthy',
        'No concerns',
        'All vitals normal',
        'Completed'
    ),
    (
        2,
        5,
        '2026-08-03',
        '09:00:00',
        'In-Person',
        'Skin rash',
        'Allergic dermatitis',
        'Prescribed antihistamine',
        'Rash reducing',
        'Completed'
    ),
    (
        2,
        3,
        '2026-09-01',
        '14:00:00',
        'Video',
        'Child vaccination',
        NULL,
        NULL,
        NULL,
        'Scheduled'
    ),
    (
        3,
        2,
        '2026-07-20',
        '15:00:00',
        'In-Person',
        'Knee pain post-surgery',
        'Recovering well',
        'Physiotherapy advised',
        'Mobility improving',
        'Completed'
    ),
    (
        3,
        2,
        '2026-08-25',
        '15:30:00',
        'In-Person',
        'Follow-up knee check',
        NULL,
        NULL,
        NULL,
        'Scheduled'
    ),
    (
        4,
        4,
        '2026-08-05',
        '10:30:00',
        'In-Person',
        'First visit, general fatigue',
        'Mild anemia',
        'Iron supplements prescribed',
        'Blood test pending',
        'Completed'
    ),
    (
        5,
        4,
        '2026-08-02',
        '08:00:00',
        'Home Visit',
        'High fever, critical',
        'Suspected infection',
        'Admitted for observation',
        'Under monitoring',
        'Completed'
    ),
    (
        6,
        1,
        '2026-08-10',
        '12:00:00',
        'In-Person',
        'Diabetes routine check',
        'Stable',
        'Continue current medication',
        'Sugar levels stable',
        'Completed'
    ),
    (
        6,
        1,
        '2026-09-05',
        '12:30:00',
        'Video',
        'Diabetes follow-up',
        NULL,
        NULL,
        NULL,
        'Scheduled'
    );

-- -------------------------------------------------------------
-- prescription
-- -------------------------------------------------------------
INSERT INTO
    prescription (
        appointment_id,
        medicine_name,
        dosage,
        duration,
        instructions
    )
VALUES
    (
        1,
        'Atenolol',
        '25mg',
        '30 days',
        'Once daily after breakfast'
    ),
    (
        3,
        'Cetirizine',
        '10mg',
        '7 days',
        'Once daily at night'
    ),
    (
        5,
        'Ibuprofen',
        '400mg',
        '10 days',
        'Twice daily after food'
    ),
    (
        7,
        'Ferrous Sulphate',
        '325mg',
        '60 days',
        'Once daily with vitamin C'
    ),
    (
        8,
        'Amoxicillin',
        '500mg',
        '7 days',
        'Three times daily'
    ),
    (
        9,
        'Metformin',
        '500mg',
        '90 days',
        'Twice daily before meals'
    );

-- -------------------------------------------------------------
-- billing
-- -------------------------------------------------------------
INSERT INTO
    billing (
        appointment_id,
        patient_id,
        total_amount,
        amount_paid,
        discount,
        refund_amount,
        claim_number,
        insurance_provider,
        total_claim_amount,
        total_insurance_amount,
        claim_status,
        invoice_number,
        ai_summary,
        status,
        rejection_reason,
        bill_date,
        due_date
    )
VALUES
    (
        1,
        1,
        1500.00,
        1500.00,
        0.00,
        0.00,
        'CLM-3001',
        'Star Health',
        1500.00,
        1200.00,
        'Accepted',
        'INV-4001',
        'Cardiology consult, claim approved.',
        'Paid',
        NULL,
        '2026-08-01',
        '2026-08-15'
    ),
    (
        2,
        1,
        800.00,
        800.00,
        0.00,
        0.00,
        NULL,
        NULL,
        0.00,
        0.00,
        'Pending',
        'INV-4002',
        'Routine checkup, no claim filed.',
        'Paid',
        NULL,
        '2026-08-15',
        '2026-08-29'
    ),
    (
        3,
        2,
        1200.00,
        600.00,
        100.00,
        0.00,
        'CLM-3002',
        'HDFC Ergo',
        1200.00,
        900.00,
        'Pending',
        'INV-4003',
        'Dermatology visit, claim under review.',
        'Partially Paid',
        NULL,
        '2026-08-03',
        '2026-08-17'
    ),
    (
        5,
        3,
        3000.00,
        3000.00,
        0.00,
        0.00,
        'CLM-3003',
        'ICICI Lombard',
        3000.00,
        2500.00,
        'Accepted',
        'INV-4004',
        'Post-surgery follow-up, claim approved.',
        'Paid',
        NULL,
        '2026-07-20',
        '2026-08-03'
    ),
    (
        7,
        4,
        900.00,
        0.00,
        0.00,
        0.00,
        NULL,
        NULL,
        0.00,
        0.00,
        'Pending',
        'INV-4005',
        'First visit, self-pay.',
        'Pending',
        NULL,
        '2026-08-05',
        '2026-08-19'
    ),
    (
        8,
        5,
        5000.00,
        2000.00,
        0.00,
        0.00,
        'CLM-3004',
        'Star Health',
        5000.00,
        3000.00,
        'Rejected',
        'INV-4006',
        'Admission claim rejected, resubmission needed.',
        'Payment Failed',
        'Missing pre-authorization',
        '2026-08-02',
        '2026-08-16'
    ),
    (
        9,
        6,
        700.00,
        700.00,
        0.00,
        0.00,
        'CLM-3005',
        'HDFC Ergo',
        700.00,
        700.00,
        'Accepted',
        'INV-4007',
        'Routine diabetic checkup, claim approved.',
        'Paid',
        NULL,
        '2026-08-10',
        '2026-08-24'
    );

-- -------------------------------------------------------------
-- activity_log
-- -------------------------------------------------------------
INSERT INTO
    activity_log (
        user_type,
        user_id,
        action,
        target_table,
        target_id,
        old_value,
        new_value,
        ip_address
    )
VALUES
    (
        'Doctor',
        1,
        'UPDATE',
        'appointment',
        1,
        'status=Scheduled',
        'status=Completed',
        '192.168.1.10'
    ),
    (
        'Patient',
        1,
        'CREATE',
        'appointment',
        2,
        NULL,
        'new appointment booked',
        '192.168.1.20'
    ),
    (
        'Doctor',
        4,
        'UPDATE',
        'billing',
        5,
        'status=Pending',
        'status=Pending',
        '192.168.1.11'
    ),
    (
        'Patient',
        5,
        'UPDATE',
        'patient',
        5,
        'is_critical=0',
        'is_critical=1',
        '192.168.1.21'
    ),
    (
        'Doctor',
        2,
        'CREATE',
        'prescription',
        3,
        NULL,
        'new prescription added',
        '192.168.1.12'
    );