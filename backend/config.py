# config.py
# This file stores all application-level settings for CareSync.
# Storing settings in one place means you only need to change one file
# when a setting changes, rather than searching through the entire codebase.

# Application identity
APP_NAME = "CareBridge"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A web-based healthcare management system designed to connect patients, doctors, and billing staff in one platform."

# Database connection settings
# In a real deployment, these values would come from environment variables
# and would never be written directly into the code.
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_NAME = "carebridge_db"
DATABASE_USER = "carebridge_user"

# User role definitions
# These constants define the three user types in the CareSync system.
ROLE_PATIENT = "patient"
ROLE_DOCTOR = "doctor"
ROLE_BILLING = "billing_staff"
ROLE_DIGITALCONSULTANT = "digital_consultant"
ROLE_APPOINTMENT = "appointment"
ROLE_ACTIVITYLOG = "activity_log"


# Pagination settings
# Controls how many records are returned per page in list views.
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
