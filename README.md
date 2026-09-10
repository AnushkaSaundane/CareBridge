# CareBridge

## Project Overview

CareBridge is a healthcare management system that helps manage patients, doctors, appointments and billing information in one place. It also provides analytics through different charts to make the data easier to understand.

The project has a backend API connected to a MySQL database and a dashboard for viewing the information.

## Technology Stack

* Python
* FastAPI
* MySQL
* Vue.js
* Chart.js

## API Endpoints

The following APIs are available in the project:

| Method | Endpoint                              | Purpose                                   |
| ------ | ------------------------------------- | ----------------------------------------- |
| GET    | `/`                                   | Checks whether the backend is running     |
| GET    | `/summary`                            | Shows basic summary information           |
| GET    | `/patients`                           | Gets the list of patients                 |
| GET    | `/patients/{patient_id}`              | Gets details of a particular patient      |
| GET    | `/patients/{patient_id}/appointments` | Gets appointments of a particular patient |
| GET    | `/billing`                            | Gets billing information                  |
| GET    | `/doctors`                            | Gets the list of doctors                  |
| GET    | `/analytics/doctors`                  | Shows doctor appointment data             |
| GET    | `/analytics/heatmap`                  | Shows appointments by day                 |
| GET    | `/analytics/revenue`                  | Shows monthly revenue                     |
| GET    | `/analytics/blood-group`              | Shows patient count based on blood group  |

## Dashboard Charts

The dashboard includes charts for:

* Doctor appointments
* Appointment heatmap
* Monthly revenue
* Patient blood groups

These charts use data received from the backend APIs.

## How to Run

### 1. Start MySQL

Make sure MySQL is running and the `carebridge` database is available.

### 2. Start the Backend

Open Command Prompt or PowerShell and go to the backend folder:

```text
cd D:\LEAD\CareBridge\backend
```

Run the FastAPI server:

```text
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

You can also check the API documentation at:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the Dashboard

Open the frontend/dashboard in the browser using the project's frontend setup.

If it is being served locally on port 5500, open:

```text
http://127.0.0.1:5500
```

## Project Structure

```text
CareBridge/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   └── config_example.py
│
├── Database/
│   ├── schema.sql
│   └── seed_data/
│
└── frontend/
```

## Summary

CareBridge combines patient, doctor, appointment and billing data with a dashboard and analytics. The backend provides APIs to get the required data, while the dashboard displays the information in a simple way.
# CareBridge – Patient Healthcare Management System

CareBridge is a healthcare management system designed to manage patient, doctor, appointment, and billing information in one place.

The system provides a FastAPI backend connected to a MySQL database and a web-based dashboard for viewing healthcare data and analytics.

## 📌 Project Overview

CareBridge helps organize healthcare information and provides useful analytics through an interactive dashboard.

The project includes:

- Patient information management
- Doctor information management
- Appointment information
- Billing information
- Patient appointment history
- Doctor appointment analytics
- Appointment heatmap
- Monthly revenue analytics
- Blood group distribution
- Patient search
- Dashboard-based data visualization

## ✨ Key Features

### 👨‍⚕️ Doctor Management
- View doctor information
- View appointment statistics
- Analyze doctor appointment volume

### 🧑‍🤝‍🧑 Patient Management
- View patient list
- Search for patients
- View individual patient details
- View patient appointment history

### 📅 Appointment Management
- Retrieve appointment information
- Analyze appointments by day
- Visualize appointment activity using a heatmap

### 💰 Billing
- Retrieve billing information
- Display monthly revenue
- Analyze billing and revenue data

### 📊 Analytics Dashboard
The dashboard provides visual analytics for:

- Doctor appointment summary
- Appointment heatmap
- Monthly revenue
- Blood group distribution
- Patient search

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend development |
| FastAPI | REST API |
| MySQL | Database |
| Vue.js | Frontend/dashboard |
| Chart.js | Data visualization |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Frontend functionality |

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Checks whether the backend is running |
| GET | `/summary` | Returns basic summary information |
| GET | `/patients` | Gets the list of patients |
| GET | `/patients/{patient_id}` | Gets details of a particular patient |
| GET | `/patients/{patient_id}/appointments` | Gets appointments of a particular patient |
| GET | `/billing` | Gets billing information |
| GET | `/doctors` | Gets the list of doctors |
| GET | `/analytics/doctors` | Returns doctor appointment analytics |
| GET | `/analytics/heatmap` | Returns appointment data by day |
| GET | `/analytics/revenue` | Returns monthly revenue data |
| GET | `/analytics/blood-group` | Returns patient count by blood group |

## 📊 Dashboard Analytics

The dashboard connects to the FastAPI backend and displays data using charts.

### Doctor Appointment Summary
Displays appointment volume for doctors.

### Appointment Heatmap
Shows the distribution of appointments across different days.

### Monthly Revenue
Displays revenue data by month.

### Blood Group Distribution
Shows the number of patients belonging to each blood group.

### Patient Search
Allows users to search for patient information.

## 🗄️ Database

CareBridge uses **MySQL** as its database.

The database contains information related to:

- Doctors
- Patients
- Appointments
- Prescriptions
- Billing
- Activity logs
- Digital consultants

The database schema and seed data are available in the `Database` folder.

## 🔗 Backend–Frontend Connectivity

The frontend dashboard communicates with the FastAPI backend through REST APIs.

```text
Frontend Dashboard
       │
       │ HTTP Requests
       ▼
FastAPI Backend
       │
       │ SQL Queries
       ▼
MySQL Database
       │
       ▼
Healthcare Data