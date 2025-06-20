const form = document.querySelector('form');
form.onsubmit = function(e) {
  const pwd = document.getElementById("new_password").value;
  const cpwd = document.getElementById("confirm_password").value;
  if (pwd !== cpwd) {
    alert("Passwords do not match!");
    e.preventDefault();
  }
};