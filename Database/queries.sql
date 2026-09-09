-- =============================================================
-- CareBridge queries.sql
-- Milestone 9: Doctor Appointment Summary query
-- Milestone 10: View built from that query
-- =============================================================
USE carebridge;

-- -------------------------------------------------------------
-- Milestone 2: Database Verifiaction
-- ALL 5 Tables visible in MySql.
-- Row counts match expected seed values.
-- Screenshot saved in the screenshots folder.
-- -------------------------------------------------------------
Show tables;

select
    count(*) as patient_count
from
    patient;

select
    count(*) as appoinment_count
from
    appointment;

-- -------------------------------------------------------------
-- Milestone 5: Sql Views Verified in Database
-- At least 2 views visible in SHOW FULL TABLES output.
-- SELECT on each view returns correct data.
-- -------------------------------------------------------------
SHOW FULL TABLES
WHERE
    Table_type = 'VIEW';

-- -------------------------------------------------------------
-- Milestone 9: Doctor Appointment Summary
-- Shows each doctor's name and their total number of appointments,
-- ordered from highest to lowest.
-- -------------------------------------------------------------
SELECT
    d.full_name AS doctor_name,
    COUNT(a.appointment_id) AS total_appointments
FROM
    doctor d
    JOIN appointment a ON a.doctor_id = d.doctor_id
GROUP BY
    d.full_name
ORDER BY
    total_appointments DESC;

-- -------------------------------------------------------------
-- Milestone 10: View vw_doctor_appointment_summary
-- Same query, saved as a reusable view.
-- -------------------------------------------------------------
SELECT
    *
FROM
    vw_doctor_appointment_summary
LIMIT
    10;

SELECT
    *
FROM
    vw_patient_appointment_history
LIMIT
    10;

SELECT
    *
FROM
    vw_billing_status_summary
LIMIT
    10;