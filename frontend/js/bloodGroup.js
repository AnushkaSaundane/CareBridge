// ============================================
// BLOOD GROUP DISTRIBUTION CHART
// ============================================

async function loadBloodGroupDistribution() {
  try {
    let data;

    if (USE_MOCK_DATA) {
      data = MOCK_BLOOD_GROUP;
    } else {
      const response = await fetch(`${API_BASE_URL}/analytics/blood-group`);
      data = await response.json();
    }

    const labels = data.map(item => item.blood_group);
    const values = data.map(item => item.count);

    const ctx = document.getElementById('bloodGroupChart').getContext('2d');
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Patients',
          data: values,
          backgroundColor: [
            '#2c3e50', '#e67e22', '#27ae60', '#c0392b',
            '#8e44ad', '#16a085', '#f39c12', '#2980b9'
          ]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Blood Group Distribution' }
        }
      }
    });
  } catch (error) {
    console.error("Error loading blood group distribution:", error);
  }
}
