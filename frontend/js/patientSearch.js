// ============================================
// PATIENT SEARCH (Milestone 8)
// ============================================

async function searchPatient() {
  const patientId = document.getElementById('patientIdInput').value.trim();
  const resultDiv = document.getElementById('patientResult');

  if (!patientId) {
    resultDiv.innerHTML = "<p>Please enter a Patient ID.</p>";
    return;
  }

  try {
    let data;

    if (USE_MOCK_DATA) {
      // Simulate a 404 when ID is 99999, for testing the error path
      if (patientId === "99999") {
        resultDiv.innerHTML = "<p class='error-text'>Patient not found</p>";
        return;
      }
      data = MOCK_PATIENT;
    } else {
      const response = await fetch(`${API_BASE_URL}/patients/${patientId}`);

      if (response.status === 404) {
        resultDiv.innerHTML = "<p class='error-text'>Patient not found</p>";
        return;
      }

      data = await response.json();
    }

    resultDiv.innerHTML = `
      <p><strong>Name:</strong> ${data.full_name}</p>
      <p><strong>Blood Group:</strong> ${data.blood_group}</p>
      <p><strong>Email:</strong> ${data.email}</p>
    `;
  } catch (error) {
    resultDiv.innerHTML = "<p class='error-text'>Something went wrong. Check the console.</p>";
    console.error(error);
  }
}