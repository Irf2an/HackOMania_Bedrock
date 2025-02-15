document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

    function showMessage(elementId, message, isSuccess) {
        const messageElement = document.getElementById(elementId);
        messageElement.innerText = message;
        messageElement.classList.remove("error-message", "success-message");

        if (isSuccess) {
            messageElement.classList.add("success-message");
        } else {
            messageElement.classList.add("error-message");
        }
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            showMessage("registerMessage", data.message || data.error, response.ok);

            if (response.ok) {
                setTimeout(() => {
                    window.location.href = "/login";
                }, 2000);
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const username = document.getElementById("loginUsername").value;
            const password = document.getElementById("loginPassword").value;

            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            showMessage("loginMessage", data.message || data.error, response.ok);

            if (response.ok) {
                localStorage.setItem("token", data.token);
                setTimeout(() => {
                    window.location.href = "/";
                }, 2000);
            }
        });
    }
});
