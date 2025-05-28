function loadCaptcha() {
    fetch("/generate_captcha")
        .then(response => response.json())
        .then(data => {
            document.getElementById("captcha-image").src = data.captcha_url + "?" + new Date().getTime();
        });
}

function refreshCaptcha() {
    loadCaptcha();
}

function verifyCaptcha() {
    let captchaAnswer = document.getElementById("captcha-input").value;

    fetch("/verify_captcha", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "captcha=" + encodeURIComponent(captchaAnswer)
    })
    .then(response => response.json())
    .then(data => {
        let messageElement = document.getElementById("captcha-message");
        messageElement.innerText = data.message;
        messageElement.style.color = data.success ? "green" : "red";
        if (data.success) {
            loadCaptcha();  // Load a new CAPTCHA on success
            document.getElementById("captcha-input").value = "";  // Clear input
        }
    });
}

// Load CAPTCHA on page load
window.onload = loadCaptcha;
