(function () {
    const BACKEND_URL = window.BACKEND_URL || "http://127.0.0.1:5000";
    const socket = io(BACKEND_URL, {
        transports: ["websocket", "polling"]
    });

    const keyPanel = document.getElementById("keyPanel");
    const challengePanel = document.getElementById("challengePanel");
    const signaturePanel = document.getElementById("signaturePanel");
    const resultPanel = document.getElementById("resultPanel");
    const resultCard = document.getElementById("resultCard");
    const timeline = document.getElementById("timeline");
    const connectionState = document.getElementById("connectionState");
    const activeUser = document.getElementById("activeUser");
    const latestEvent = document.getElementById("latestEvent");
    const eventCount = document.getElementById("eventCount");
    const transportState = document.getElementById("transportState");
    let totalEvents = 0;

    function wireExternalSiteLinks() {
        const siteLinks = window.SITE_LINKS || {};
        document.querySelectorAll("[data-site-link]").forEach(function (link) {
            const siteName = link.getAttribute("data-site-link");
            const baseUrl = siteLinks[siteName];
            if (!baseUrl) {
                return;
            }
            link.href = `${baseUrl.replace(/\/$/, "")}/index.html`;
        });
    }

    function typeText(element, text) {
        element.textContent = "";
        let index = 0;
        const timer = window.setInterval(function () {
            element.textContent += text.charAt(index);
            index += 1;
            if (index >= text.length) {
                window.clearInterval(timer);
            }
        }, 10);
    }

    function addTimeline(title, content) {
        const item = document.createElement("div");
        item.className = "timeline-item";
        item.innerHTML = `<strong>${title}</strong><span>${content}</span>`;
        timeline.prepend(item);
    }

    function recordEvent(label, username) {
        totalEvents += 1;
        eventCount.textContent = String(totalEvents);
        latestEvent.textContent = label;
        if (username) {
            activeUser.textContent = username;
        }
        if (socket.io && socket.io.engine && socket.io.engine.transport) {
            transportState.textContent = socket.io.engine.transport.name;
        }
    }

    wireExternalSiteLinks();

    socket.on("connect", function () {
        connectionState.textContent = "Socket connected";
        connectionState.classList.add("is-online");
        connectionState.classList.remove("is-offline");
        addTimeline("Connection", "Demo monitor connected to backend websocket.");
        recordEvent("Connected", "");
    });

    socket.on("disconnect", function () {
        connectionState.textContent = "Socket disconnected";
        connectionState.classList.add("is-offline");
        connectionState.classList.remove("is-online");
        addTimeline("Connection", "Demo monitor lost websocket connection.");
        latestEvent.textContent = "Disconnected";
    });

    socket.on("key_generated", function (payload) {
        const content = `User: ${payload.username}\nPublic Key: ${payload.public_key}\nSecret Key: ${payload.secret_key}`;
        typeText(keyPanel, content);
        addTimeline("Key Generated", `User ${payload.username} received a new public/secret key pair.`);
        recordEvent("Key Generated", payload.username);
    });

    socket.on("challenge_created", function (payload) {
        const content = `User: ${payload.username}\nChallenge: ${payload.challenge}`;
        typeText(challengePanel, content);
        addTimeline("Challenge Created", `Challenge issued for ${payload.username}.`);
        recordEvent("Challenge Created", payload.username);
    });

    socket.on("signature_generated", function (payload) {
        const content = `User: ${payload.username}\nChallenge: ${payload.challenge}\nSignature: ${payload.signature}`;
        typeText(signaturePanel, content);
        addTimeline("Signature Generated", `Signature captured for ${payload.username}.`);
        recordEvent("Signature Generated", payload.username);
    });

    socket.on("auth_success", function (payload) {
        resultCard.classList.add("is-success");
        resultCard.classList.remove("is-failed");
        typeText(resultPanel, `User: ${payload.username}\nStatus: SUCCESS\nAuthentication completed successfully.`);
        addTimeline("Authentication Success", `${payload.username} authenticated successfully.`);
        recordEvent("Authentication Success", payload.username);
    });

    socket.on("auth_failed", function (payload) {
        resultCard.classList.add("is-failed");
        resultCard.classList.remove("is-success");
        typeText(resultPanel, `User: ${payload.username}\nStatus: FAILED\nReason: ${payload.reason}`);
        addTimeline("Authentication Failed", `${payload.username} failed authentication: ${payload.reason}`);
        recordEvent("Authentication Failed", payload.username);
    });
})();
