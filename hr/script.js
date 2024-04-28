// script.js
document.getElementById("getStarted").addEventListener("click", function () {
  document.getElementById("modal").style.display = "block";
});

document
  .getElementsByClassName("close")[0]
  .addEventListener("click", function () {
    document.getElementById("modal").style.display = "none";
  });

window.onclick = function (event) {
  if (event.target == document.getElementById("modal")) {
    document.getElementById("modal").style.display = "none";
  }
};
document.addEventListener("DOMContentLoaded", function () {
  var loginButton = document.querySelector(".navbar-login-button");
  loginButton.addEventListener("click", function () {
    window.location.href = "login.html";
  });
});
document.getElementById("department").addEventListener("change", function () {
  const department = this.value;
  // Assuming function fetchCompetencies is defined to fetch from backend
  fetchCompetencies(department).then((competencies) => {
    const displayArea = document.getElementById("competency-display");
    displayArea.innerHTML = competencies
      .map((comp) => `<div class="competency">${comp.name}</div>`)
      .join("");
  });
});
