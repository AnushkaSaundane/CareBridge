-- =============================================================
-- CareBridge Patient Portal
-- Database Schema  v2  (updated per handwritten design notes)
-- MySQL 8.0
-- =============================================================
-- CHANGE SUMMARY vs v1:
--  * NEW  digital_consultant  -> home visit / video / emergency
--                                availability, tied to doctor
--  * NEW  prescription        -> medicines per appointment
--  * doctor   -> removed AI/consult/clinical-notes fields (now live
--                on digital_consultant / appointment); added
--                qualification, address, experience, joining_date,
--                working_days
--  * patient  -> added insurance fields, ai_summary, and status flags
--                (home visit request, follow-up, admitted, critical,
--                allergies)
--  * billing  -> added claim / invoice / insurance fields, refund +
--                payment-failed status, link to billing_staff
-- =============================================================
CREATE DATABASE IF NOT EXISTS carebridge CHARACTER
SET
    utf8mb4 COLLATE utf8mb4_unicode_ci;

USE carebridge;

SET
    FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS activity_log;

DROP TABLE IF EXISTS prescription;

DROP TABLE IF EXISTS billing;

DROP TABLE IF EXISTS appointment;

DROP TABLE IF EXISTS digital_consultant;

DROP TABLE IF EXISTS patient;

DROP TABLE IF EXISTS doctor;

SET
    FOREIGN_KEY_CHECKS = 1;

-- -------------------------------------------------------------
-- Table: doctor
-- -------------------------------------------------------------
CREATE TABLE
    doctor (
        doctor_id INT NOT NULL AUTO_INCREMENT,
        full_name VARCHAR(150) NOT NULL,
        department VARCHAR(100),
        specialisation VARCHAR(100) NOT NULL,
        qualification VARCHAR(150),
        experience_years INT DEFAULT 0,
        phone VARCHAR(15),
        email VARCHAR(150),
        address TEXT,
        licence_number VARCHAR(50) NOT NULL,
        working_days VARCHAR(100) COMMENT 'e.g. Mon,Tue,Wed,Thu,Fri',
        joining_date DATE,
        is_active TINYINT (1) NOT NULL DEFAULT 1,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (doctor_id),
        UNIQUE KEY uq_doctor_email (email),
        UNIQUE KEY uq_doctor_licence (licence_number)
    );

-- -------------------------------------------------------------
-- Table: digital_consultant
-- One row per doctor describing their remote/on-call availability
-- -------------------------------------------------------------
CREATE TABLE
    digital_consultant (
        consultant_id INT NOT NULL AUTO_INCREMENT,
        doctor_id INT NOT NULL,
        home_visit_available ENUM ('Yes', 'No') NOT NULL DEFAULT 'No',
        video_consult_available ENUM ('Yes', 'No') NOT NULL DEFAULT 'No',
        emergency_available ENUM ('Yes', 'No') NOT NULL DEFAULT 'No',
        available_today TINYINT (1) NOT NULL DEFAULT 0,
        available_slots_today INT NOT NULL DEFAULT 0,
        on_leave TINYINT (1) NOT NULL DEFAULT 0,
        is_verified TINYINT (1) NOT NULL DEFAULT 0,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (consultant_id),
        UNIQUE KEY uq_consultant_doctor (doctor_id),
        CONSTRAINT fk_consultant_doctor FOREIGN KEY (doctor_id) REFERENCES doctor (doctor_id) ON DELETE CASCADE ON UPDATE CASCADE,
        INDEX idx_consultant_available_today (available_today),
        INDEX idx_consultant_on_leave (on_leave)
    );

-- -------------------------------------------------------------
-- Table: patient
-- -------------------------------------------------------------
CREATE TABLE
    patient (
        patient_id INT NOT NULL AUTO_INCREMENT,
        full_name VARCHAR(150) NOT NULL,
        date_of_birth DATE NOT NULL,
        gender ENUM ('Male', 'Female', 'Other') NOT NULL,
        phone VARCHAR(15),
        email VARCHAR(150),
        address TEXT,
        blood_group VARCHAR(5),
        emergency_contact_name VARCHAR(150),
        emergency_contact_phone VARCHAR(15),
        -- insurance
        insurance_provider VARCHAR(150),
        insurance_policy_no VARCHAR(50),
        -- AI summary of patient history/records
        ai_summary TEXT,
        -- status flags (from notes)
        home_visit_requested TINYINT (1) NOT NULL DEFAULT 0,
        follow_up_required TINYINT (1) NOT NULL DEFAULT 0,
        is_admitted TINYINT (1) NOT NULL DEFAULT 0,
        is_critical TINYINT (1) NOT NULL DEFAULT 0,
        has_allergies TINYINT (1) NOT NULL DEFAULT 0,
        allergy_details TEXT,
        is_deleted TINYINT (1) NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (patient_id),
        INDEX idx_patient_name (full_name),
        INDEX idx_patient_status (is_admitted, is_critical)
    );

-- -------------------------------------------------------------
-- Table: appointment
-- -------------------------------------------------------------
CREATE TABLE
    appointment (
        appointment_id INT NOT NULL AUTO_INCREMENT,
        patient_id INT NOT NULL,
        doctor_id INT NOT NULL,
        appointment_date DATE NOT NULL,
        appointment_time TIME NOT NULL,
        consult_mode ENUM ('In-Person', 'Video', 'Home Visit') NOT NULL DEFAULT 'In-Person',
        reason TEXT,
        diagnosis TEXT,
        notes TEXT,
        report_summary TEXT,
        status ENUM ('Scheduled', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Scheduled',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (appointment_id),
        CONSTRAINT fk_appt_patient FOREIGN KEY (patient_id) REFERENCES patient (patient_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_appt_doctor FOREIGN KEY (doctor_id) REFERENCES doctor (doctor_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        INDEX idx_appt_patient (patient_id),
        INDEX idx_appt_doctor (doctor_id),
        INDEX idx_appt_date (appointment_date)
    );

-- -------------------------------------------------------------
-- Table: prescription  (medicines per appointment)
-- -------------------------------------------------------------
CREATE TABLE
    prescription (
        prescription_id INT NOT NULL AUTO_INCREMENT,
        appointment_id INT NOT NULL,
        medicine_name VARCHAR(150) NOT NULL,
        dosage VARCHAR(100),
        duration VARCHAR(100),
        instructions TEXT,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (prescription_id),
        CONSTRAINT fk_prescription_appointment FOREIGN KEY (appointment_id) REFERENCES appointment (appointment_id) ON DELETE CASCADE ON UPDATE CASCADE,
        INDEX idx_prescription_appointment (appointment_id)
    );

-- -------------------------------------------------------------
-- Table: billing
-- -------------------------------------------------------------
CREATE TABLE
    billing (
        bill_id INT NOT NULL AUTO_INCREMENT,
        appointment_id INT NOT NULL,
        patient_id INT NOT NULL,
        total_amount DECIMAL(10, 2) NOT NULL,
        amount_paid DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
        discount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
        refund_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
        -- insurance claim fields
        claim_number VARCHAR(50),
        insurance_provider VARCHAR(150),
        total_claim_amount DECIMAL(10, 2) DEFAULT 0.00,
        total_insurance_amount DECIMAL(10, 2) DEFAULT 0.00,
        claim_status ENUM ('Pending', 'Accepted', 'Rejected') DEFAULT 'Pending',
        invoice_number VARCHAR(50),
        ai_summary TEXT,
        status ENUM (
            'Pending',
            'Paid',
            'Partially Paid',
            'Payment Failed',
            'Refund',
            'Rejected'
        ) NOT NULL DEFAULT 'Pending',
        rejection_reason TEXT,
        bill_date DATE NOT NULL,
        due_date DATE,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (bill_id),
        UNIQUE KEY uq_bill_appointment (appointment_id),
        CONSTRAINT fk_bill_appointment FOREIGN KEY (appointment_id) REFERENCES appointment (appointment_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_bill_patient FOREIGN KEY (patient_id) REFERENCES patient (patient_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        INDEX idx_bill_patient (patient_id),
        INDEX idx_bill_status (status),
        INDEX idx_bill_date (bill_date),
        INDEX idx_bill_claim_status (claim_status)
    );

-- -------------------------------------------------------------
-- Table: activity_log
-- -------------------------------------------------------------
CREATE TABLE
    activity_log (
        log_id BIGINT NOT NULL AUTO_INCREMENT,
        user_type ENUM ('Doctor', 'Patient', 'Billing') NOT NULL,
        user_id INT NOT NULL,
        action VARCHAR(100) NOT NULL,
        target_table VARCHAR(50),
        target_id INT,
        old_value TEXT,
        new_value TEXT,
        ip_address VARCHAR(45),
        logged_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (log_id),
        INDEX idx_log_user (user_type, user_id),
        INDEX idx_log_action (action),
        INDEX idx_log_time (logged_at)
    );