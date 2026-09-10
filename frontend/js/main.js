// ============================================
// MAIN ENTRY POINT
// Runs once the page has loaded.
// ============================================

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  loadRevenueTrend();
  loadHeatmap();
  loadBloodGroupDistribution();
  loadDoctorSummary();
});
