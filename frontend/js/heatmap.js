// ============================================
// APPOINTMENT HEATMAP CHART
// (rendered as a bar chart by day of week)
// ============================================

async function loadHeatmap() {
  try {
    let data;

    if (USE_MOCK_DATA) {
      data = MOCK_HEATMAP;
    } else {
      const response = await fetch(`${API_BASE_URL}/analytics/heatmap`);
      data = await response.json();
    }

    const labels = data.map(item => item.day);
    const values = data.map(item => item.appointments);

    const ctx = document.getElementById('heatmapChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Appointments',
          data: values,
          backgroundColor: 'rgba(230, 126, 34, 0.7)'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Appointments by Day of Week' }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (error) {
    console.error("Error loading heatmap:", error);
  }
}
