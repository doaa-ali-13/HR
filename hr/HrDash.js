function showModal() {
  document.getElementById("employee-modal").style.display = "block";
}

function hideModal() {
  document.getElementById("employee-modal").style.display = "none";
}

function addEmployee(event) {
  event.preventDefault();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  // Assume function to interact with backend here
  console.log("Submit employee data to backend");
  hideModal();
  alert("Employee added successfully!");
}
