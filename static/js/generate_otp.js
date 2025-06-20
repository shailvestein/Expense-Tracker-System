// Refresh detection
let isRefresh = false;
const navEntries = performance.getEntriesByType("navigation");
if (navEntries.length > 0 && navEntries[0].type === "reload") {
  isRefresh = true;
} else if (performance.navigation && performance.navigation.type === 1) {
  isRefresh = true;
}

if (isRefresh) {
  window.location.href = "{{ url_for('generate_otp') }}";
}

// Timer
let timeLeft = 60;
const timerDisplay = document.getElementById("timer");
const validateBtn = document.getElementById("validate_otp_btn");
const cancelBtn = document.getElementById("cancel_btn");

const countdown = setInterval(() => {
  if (timeLeft <= 0) {
    clearInterval(countdown);
    if (timerDisplay) {
      timerDisplay.innerHTML = "⛔ OTP expired. Please request again.";
    }
    if (validateBtn) {
      validateBtn.disabled = true;
    }
    if (cancelBtn) {
      cancelBtn.innerText = "Request OTP Again";
      cancelBtn.href = "{{ url_for('generate_otp') }}";
    }
  } else {
    if (timerDisplay) {
      timerDisplay.innerHTML = `⏳ OTP valid for: ${timeLeft} seconds`;
    }
    timeLeft--;
  }
}, 1000);