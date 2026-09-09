// ============================================
// MOCK DATA
// Replace field names here once Rutuja confirms
// exact JSON shape her API returns. Remove or
// ignore this file once USE_MOCK_DATA = false.
// ============================================

const MOCK_PATIENT = {
  patient_id: 101,
  name: "Asha Patil",
  blood_group: "B+",
  email: "asha.patil@example.com"
};

const MOCK_DOCTOR_SUMMARY = [
  { doctor_name: "Dr. Mehta", appointment_count: 45 },
  { doctor_name: "Dr. Kulkarni", appointment_count: 38 },
  { doctor_name: "Dr. Rao", appointment_count: 29 },
  { doctor_name: "Dr. Shah", appointment_count: 52 },
  { doctor_name: "Dr. Iyer", appointment_count: 33 }
];

const MOCK_REVENUE_TREND = [
  { month: "Jan", revenue: 120000 },
  { month: "Feb", revenue: 135000 },
  { month: "Mar", revenue: 128000 },
  { month: "Apr", revenue: 150000 },
  { month: "May", revenue: 142000 },
  { month: "Jun", revenue: 160000 }
];

const MOCK_HEATMAP = [
  { day: "Mon", appointments: 40 },
  { day: "Tue", appointments: 55 },
  { day: "Wed", appointments: 48 },
  { day: "Thu", appointments: 62 },
  { day: "Fri", appointments: 58 },
  { day: "Sat", appointments: 30 },
  { day: "Sun", appointments: 15 }
];

const MOCK_BLOOD_GROUP = [
  { blood_group: "A+", count: 120 },
  { blood_group: "B+", count: 95 },
  { blood_group: "O+", count: 150 },
  { blood_group: "AB+", count: 40 },
  { blood_group: "A-", count: 25 },
  { blood_group: "B-", count: 20 },
  { blood_group: "O-", count: 35 },
  { blood_group: "AB-", count: 15 }
];
