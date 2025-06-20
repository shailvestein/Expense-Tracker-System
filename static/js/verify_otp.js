// --- Detect Page Refresh ---
let navType = "unknown";

if (performance.getEntriesByType("navigation").length > 0) {
  navType = performance.getEntriesByType("navigation")[0].type;
} else if (performance.navigation && performance.navigation.type === 1) {
  navType = "reload";
}

if (navType === "reload") {
  // Redirect on refresh
  window.location.href = "{{ url_for('generate_otp') }}";
}

// --- OTP Countdown Timer ---
let timeLeft = 60;  // 60 seconds
const timerDisplay = document.getElementById("timer");

const countdown = setInterval(() => {
  if (timeLeft <= 0) {
    clearInterval(countdown);
    timerDisplay.innerHTML = "⛔ OTP expired. Please request again.";

    const validateBtn = document.getElementById("validate_otp_btn");
    const cancelBtn = document.getElementById("cancel_btn");

    if (validateBtn) validateBtn.disabled = true;
    if (cancelBtn) {
      cancelBtn.innerText = "Request OTP Again";
      cancelBtn.href = "{{ url_for('generate_otp') }}";  // or url_for('generate_otp') if you renamed it
    }

  } else {
    timerDisplay.innerHTML = `⏳ OTP valid for: ${timeLeft} seconds`;
    timeLeft--;
  }
}, 1000);