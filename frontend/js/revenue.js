// ============================================
// REVENUE TREND CHART
// ============================================

async function loadRevenueTrend() {
  try {
    let data;

    if (USE_MOCK_DATA) {
      data = MOCK_REVENUE_TREND;
    } else {
      const response = await fetch(`${API_BASE_URL}/analytics/revenue`);
      data = await response.json();
    }

    const labels = data.map(item => item.month);
    const values = data.map(item => item.revenue);

    const ctx = document.getElementById('revenueChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Revenue (Rs.)',
          data: values,
          borderColor: '#2c3e50',
          backgroundColor: 'rgba(44, 62, 80, 0.1)',
          fill: true,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Monthly Revenue Trend' }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (error) {
    console.error("Error loading revenue trend:", error);
  }
}
