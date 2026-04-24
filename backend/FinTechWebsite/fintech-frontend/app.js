(function () {
    const BACKEND_URL = window.BACKEND_URL || "http://127.0.0.1:5000";
    const AUTH_STORAGE_KEY = "quantumpay_auth_user";
    const DEVICE_CREDENTIALS_KEY = "quantumpay_device_credentials";

    function $(id) {
        return document.getElementById(id);
    }

    function setMessage(element, text, type) {
        if (!element) {
            return;
        }
        element.textContent = text;
        element.classList.remove("is-error", "is-success");
        if (type === "error") {
            element.classList.add("is-error");
        }
        if (type === "success") {
            element.classList.add("is-success");
        }
    }

    function setButtonLoading(button, isLoading, idleLabel, loadingLabel) {
        if (!button) {
            return;
        }
        const text = button.querySelector(".button-text");
        button.disabled = isLoading;
        button.classList.toggle("is-loading", isLoading);
        if (text) {
            text.textContent = isLoading ? loadingLabel : idleLabel;
        }
    }

    function loadCredentials() {
        try {
            return JSON.parse(localStorage.getItem(DEVICE_CREDENTIALS_KEY) || "{}");
        } catch (error) {
            return {};
        }
    }

    function saveCredential(username, secretKey) {
        const credentials = loadCredentials();
        credentials[username] = btoa(unescape(encodeURIComponent(secretKey)));
        localStorage.setItem(DEVICE_CREDENTIALS_KEY, JSON.stringify(credentials));
    }

    function getCredential(username) {
        const credentials = loadCredentials();
        const value = credentials[username];
        if (!value) {
            return "";
        }
        try {
            return decodeURIComponent(escape(atob(value)));
        } catch (error) {
            return "";
        }
    }

    function validateEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }

    function sha256(value) {
        if (!window.CryptoJS) {
            throw new Error("CryptoJS failed to load.");
        }
        return window.CryptoJS.SHA256(value).toString();
    }

    function friendlyError(error) {
        const message = (error && error.message) || "Unknown error";
        if (message === "Failed to fetch" || message.includes("NetworkError")) {
            return `QuantumPay backend is offline. Start the Flask server on ${BACKEND_URL} and try again.`;
        }
        return message;
    }

    async function parseJson(response) {
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            const message = data.error || data.message || `Request failed with status ${response.status}`;
            throw new Error(message);
        }
        return data;
    }

    async function postJson(url, payload) {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        return parseJson(response);
    }

    async function checkBackendStatus() {
        const badge = $("backendStatus");
        if (!badge) {
            return;
        }
        try {
            const response = await fetch(`${BACKEND_URL}/status`, { method: "GET" });
            if (!response.ok) {
                throw new Error("Offline");
            }
            badge.textContent = "Backend connected. Registration and login are available.";
            badge.classList.add("is-online");
            badge.classList.remove("is-offline");
        } catch (error) {
            badge.textContent = `Backend offline. Start the Flask app at ${BACKEND_URL} before registering or logging in.`;
            badge.classList.add("is-offline");
            badge.classList.remove("is-online");
        }
    }

    function navigateWithTransition(url) {
        const overlay = $("pageTransition");
        if (overlay) {
            overlay.classList.add("is-active");
            window.setTimeout(function () {
                window.location.href = url;
            }, 240);
            return;
        }
        window.location.href = url;
    }

    function wirePageTransitions() {
        document.querySelectorAll("a[href$='.html']").forEach(function (link) {
            link.addEventListener("click", function (event) {
                const href = link.getAttribute("href");
                if (!href || href.startsWith("http")) {
                    return;
                }
                event.preventDefault();
                navigateWithTransition(href);
            });
        });
    }

    async function handleRegisterSubmit(event) {
        event.preventDefault();

        const name = $("registerName").value.trim();
        const email = $("registerEmail").value.trim();
        const phone = $("registerPhone").value.trim();
        const username = $("registerUsername").value.trim();
        const messageEl = $("registerMessage");
        const button = $("registerButton");

        if (!name || !email || !phone || !username) {
            setMessage(messageEl, "Please complete all registration fields.", "error");
            return;
        }
        if (!validateEmail(email)) {
            setMessage(messageEl, "Enter a valid email address.", "error");
            return;
        }

        setButtonLoading(button, true, "Create Secure Account", "Enrolling Device...");
        setMessage(messageEl, "Creating your account and enrolling this browser...", "");

        try {
            const registerResponse = await postJson(`${BACKEND_URL}/register`, {
                username,
                name,
                email,
                phone
            });

            if (!registerResponse.secret_key) {
                throw new Error("Registration completed but no device credential was returned.");
            }

            saveCredential(username, registerResponse.secret_key);
            sessionStorage.setItem(AUTH_STORAGE_KEY, username);
            event.target.reset();

            const emailDelivery = registerResponse.email_delivery;
            const emailSuffix = emailDelivery && !emailDelivery.sent
                ? ` Account created, but email delivery needs attention: ${emailDelivery.reason}`
                : " Account created and secret key email processing completed.";
            setMessage(messageEl, `Registration successful.${emailSuffix}`, "success");
        } catch (error) {
            setMessage(messageEl, friendlyError(error), "error");
        } finally {
            setButtonLoading(button, false, "Create Secure Account", "Enrolling Device...");
        }
    }

    async function handleLoginSubmit(event) {
        event.preventDefault();

        const username = $("loginUsername").value.trim();
        const messageEl = $("loginMessage");
        const button = $("loginButton");

        if (!username) {
            setMessage(messageEl, "Enter your username to continue.", "error");
            return;
        }

        const secretKey = getCredential(username);
        if (!secretKey) {
            setMessage(messageEl, "This browser is not enrolled for that username yet. Register on this device first.", "error");
            return;
        }

        setButtonLoading(button, true, "Authenticate", "Verifying...");
        setMessage(messageEl, "Requesting challenge and signing with your device credential...", "");

        try {
            const loginResponse = await postJson(`${BACKEND_URL}/login`, { username });
            const challenge = loginResponse.challenge;
            if (!challenge) {
                throw new Error("No challenge returned by the backend.");
            }

            const signature = sha256(`${challenge}${secretKey}`);
            const verifyResponse = await postJson(`${BACKEND_URL}/verify`, {
                username,
                message: challenge,
                signature
            });

            if (verifyResponse.result !== "VALID") {
                throw new Error(verifyResponse.error || "Authentication failed.");
            }

            sessionStorage.setItem(AUTH_STORAGE_KEY, username);
            setMessage(messageEl, "Authentication successful. Opening dashboard...", "success");
            window.setTimeout(function () {
                navigateWithTransition("./dashboard.html");
            }, 350);
        } catch (error) {
            setMessage(messageEl, friendlyError(error), "error");
        } finally {
            setButtonLoading(button, false, "Authenticate", "Verifying...");
        }
    }

    function initRegister() {
        const form = $("registerForm");
        if (form) {
            form.addEventListener("submit", handleRegisterSubmit);
        }
    }

    function initLogin() {
        const form = $("loginForm");
        if (form) {
            form.addEventListener("submit", handleLoginSubmit);
        }
    }

    function initDashboard() {
        const currentUser = sessionStorage.getItem(AUTH_STORAGE_KEY);
        if (!currentUser) {
            navigateWithTransition("./login.html");
            return;
        }
        const welcome = $("welcomeUser");
        if (welcome) {
            welcome.textContent = `Authenticated as ${currentUser}`;
        }
        const logoutButton = $("logoutButton");
        if (logoutButton) {
            logoutButton.addEventListener("click", function () {
                sessionStorage.removeItem(AUTH_STORAGE_KEY);
                navigateWithTransition("./login.html");
            });
        }
    }

    function init() {
        wirePageTransitions();
        checkBackendStatus();
        const page = document.body.dataset.page;
        if (page === "register") {
            initRegister();
        }
        if (page === "login") {
            initLogin();
        }
        if (page === "dashboard") {
            initDashboard();
        }
    }

    document.addEventListener("DOMContentLoaded", init);
})();
