-- =============================================================
-- CareBridge queries.sql
-- Milestone 9: Doctor Appointment Summary query
-- Milestone 10: View built from that query
-- =============================================================
USE carebridge;

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
CREATE
OR REPLACE VIEW vw_doctor_appointment_summary AS
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

-- Verify the view works:
-- SELECT * FROM vw_doctor_appointment_summary LIMIT 10;