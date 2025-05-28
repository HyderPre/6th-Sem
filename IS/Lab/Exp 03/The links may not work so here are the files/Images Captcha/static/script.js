let selectedImages = [];

function loadCaptcha() {
    fetch("/generate_captcha")
        .then(response => response.json())
        .then(data => {
            document.getElementById("captcha-question").innerText = "Select all images with: " + data.category;
            let container = document.getElementById("captcha-container");
            container.innerHTML = ""; // Clear old images

            selectedImages = [];

            data.images.forEach((imageUrl, index) => {
                let img = document.createElement("img");
                img.src = imageUrl + "?t=" + new Date().getTime();  // Prevent caching issues
                img.onclick = function() {
                    toggleSelection(img, imageUrl);
                };
                container.appendChild(img);
            });
        });
}

function toggleSelection(imgElement, imageUrl) {
    if (selectedImages.includes(imageUrl)) {
        selectedImages = selectedImages.filter(img => img !== imageUrl);
        imgElement.classList.remove("selected");
    } else {
        selectedImages.push(imageUrl);
        imgElement.classList.add("selected");
    }
}

function verifyCaptcha() {
    fetch("/verify_captcha", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ selectedImages: selectedImages })
    })
    .then(response => response.json())
    .then(data => {
        let messageElement = document.getElementById("captcha-message");
        messageElement.innerText = data.message;
        messageElement.style.color = data.success ? "green" : "red";
        if (data.success) {
            loadCaptcha(); // Load a new CAPTCHA on success
        }
    });
}

// Load CAPTCHA on page load
window.onload = loadCaptcha;
