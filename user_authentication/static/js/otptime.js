var countdownTimer = document.getElementById("countdown-timer");
var countdownSeconds = document.getElementById("countdown-seconds");
var otpExpiredMessage = document.getElementById("otp-expired-message");

var expirationTime = new Date("{{ request.session.otp_expiration_time }}").getTime();
var now = new Date().getTime();
var remainingTime = Math.max(0, Math.floor((expirationTime - now) / 1000));

function updateTimer() {
    if (remainingTime <= 0) {
        countdownTimer.style.display = "none"; // Hide countdown timer
        otpExpiredMessage.style.display = "block";
        clearInterval(timerInterval);
    } else {
        var minutes = Math.floor(remainingTime / 60);
        var seconds = remainingTime % 60;
        countdownSeconds.innerHTML = (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
        remainingTime--;
        localStorage.setItem("remainingTime", remainingTime);
    }
}

if (remainingTime === null) {
    remainingTime = Math.max(0, 36); // Initial remaining time
    localStorage.setItem("remainingTime", remainingTime);
}

updateTimer();
var timerInterval = setInterval(updateTimer, 1000);