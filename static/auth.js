document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

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
            document.getElementById("registerMessage").innerText = data.message || data.error;

            if (response.ok) {
                setTimeout(() => {
                    window.location.href = "login.html";
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
            document.getElementById("loginMessage").innerText = data.message || data.error;

            if (response.ok) {
                localStorage.setItem("token", data.token);
                setTimeout(() => {
                    window.location.href = "index.html";
                }, 2000);
            }
        });
    }
});
