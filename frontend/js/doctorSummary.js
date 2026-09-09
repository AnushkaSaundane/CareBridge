// ============================================
// DOCTOR SUMMARY CHART (Milestone 12)
// ============================================

async function loadDoctorSummary() {
  try {
    let data;

    if (USE_MOCK_DATA) {
      data = MOCK_DOCTOR_SUMMARY;
    } else {
      const response = await fetch(`${API_BASE_URL}/analytics/doctors`);
      data = await response.json();
    }

    const doctorNames = data.map(item => item.doctor_name);
    const appointmentCounts = data.map(item => item.appointment_count);

    const ctx = document.getElementById('doctorChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: doctorNames,
        datasets: [{
          label: 'Appointments',
          data: appointmentCounts,
          backgroundColor: 'rgba(54, 162, 235, 0.7)'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Appointments Per Doctor' }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (error) {
    console.error("Error loading doctor summary:", error);
  }
}
