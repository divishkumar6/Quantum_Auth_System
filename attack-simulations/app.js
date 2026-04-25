(function () {
    function wireExternalSiteLinks() {
        const siteLinks = window.SITE_LINKS || {};
        document.querySelectorAll("[data-site-link]").forEach(function (link) {
            const siteName = link.getAttribute("data-site-link");
            const baseUrl = siteLinks[siteName];
            if (!baseUrl) {
                return;
            }
            if (/^https?:\/\//i.test(baseUrl)) {
                link.href = baseUrl.replace(/\/$/, "");
                return;
            }
            link.href = `${baseUrl.replace(/\/$/, "")}/index.html`;
        });
    }

    const scenarios = {
        replay: {
            title: "Replay Attack",
            risk: "Medium",
            defense: "Single-use challenge",
            summary: "An attacker intercepts a previously valid signed challenge and tries to replay it later. QuantumPay prevents reuse by deleting the challenge after each verification attempt.",
            gridCaption: "The attacker reuses an old proof, but the challenge store no longer contains a valid active nonce.",
            grid: [
                ["User", "Trusted device", "trace"],
                ["Old signature", "Captured proof", "attack"],
                ["Challenge store", "Expired", "defense"],
                ["Login request", "Fresh nonce", "trace"],
                ["Verifier", "Reject replay", "focus active defense"],
                ["Audit trail", "Result logged", "trace"],
                ["Attacker", "Resubmits", "attack"],
                ["Socket demo", "Shows failure", "trace"],
                ["Defense", "Single-use", "defense"]
            ],
            attackerMoves: [
                "Observe or steal a valid signature from an earlier session.",
                "Resubmit the same challenge and signature pair later.",
                "Hope the backend still accepts the old nonce."
            ],
            systemResponse: [
                "The backend stores a fresh challenge per login request.",
                "The challenge is removed after verification, whether it succeeds or fails.",
                "A replayed challenge hits the 'challenge expired or not found' path."
            ],
            timeline: [
                ["Attacker captures a valid signed challenge.", "warning"],
                ["User session ends and the challenge is invalidated.", "success"],
                ["Replay request arrives with an old message/signature pair.", "warning"],
                ["Backend rejects the request because no active challenge exists.", "success"]
            ]
        },
        tamper: {
            title: "Message Tampering",
            risk: "High",
            defense: "Challenge integrity check",
            summary: "An attacker modifies the challenge or verification payload in transit. The backend compares the incoming message with the originally issued challenge before it accepts any proof.",
            gridCaption: "A modified message changes the request path, but the backend catches the mismatch between the stored challenge and the submitted one.",
            grid: [
                ["Client", "Receives challenge", "trace"],
                ["Network", "Payload intercepted", "attack"],
                ["Tampered msg", "Changed body", "attack active"],
                ["Challenge store", "Original value", "defense"],
                ["Verifier", "Mismatch found", "focus defense"],
                ["Response", "Rejected", "defense"],
                ["Timeline", "Incident shown", "trace"],
                ["Attacker", "Mutation attempt", "attack"],
                ["Integrity", "Protected flow", "defense"]
            ],
            attackerMoves: [
                "Intercept the login verification request.",
                "Modify the challenge value or swap the username.",
                "Forward the altered payload to the backend."
            ],
            systemResponse: [
                "The backend loads the active challenge for that username.",
                "It compares the received message against the stored challenge.",
                "A mismatch is flagged as tampering and the flow is terminated."
            ],
            timeline: [
                ["Backend issues a challenge for the real user.", "success"],
                ["Attacker mutates the message body before verification.", "danger"],
                ["Backend detects message != stored challenge.", "success"],
                ["Authentication is rejected and the challenge is burned.", "success"]
            ]
        },
        device: {
            title: "Device Theft",
            risk: "High",
            defense: "Local credential scope and user response",
            summary: "If a trusted device is stolen, the local browser credential can be abused until the account is rotated or re-enrolled. This is a realistic operational risk even when the cryptographic flow is sound.",
            gridCaption: "This is the most operationally dangerous case: the cryptography still works, but trust in the endpoint is broken.",
            grid: [
                ["Owner", "Loses device", "warning"],
                ["Browser", "Stored secret", "attack active"],
                ["Attacker", "Uses device", "attack"],
                ["Challenge", "Still fresh", "trace"],
                ["Verifier", "Proof can pass", "focus attack"],
                ["Ops response", "Rotate / revoke", "defense"],
                ["MFA gap", "Needs hardening", "warning"],
                ["Security team", "Contain incident", "defense"],
                ["Risk", "Endpoint trust", "warning"]
            ],
            attackerMoves: [
                "Gain physical access to a previously enrolled browser.",
                "Reuse the stored browser credential to answer fresh challenges.",
                "Attempt to log in before the legitimate user responds."
            ],
            systemResponse: [
                "The trusted-device design improves convenience but increases endpoint sensitivity.",
                "The current prototype needs a manual re-registration or key rotation response.",
                "A production design would add device revocation, MFA, or session controls."
            ],
            timeline: [
                ["Attacker opens the enrolled browser.", "danger"],
                ["Backend still sees a valid fresh challenge/response pair.", "warning"],
                ["Without revocation, the cryptographic proof can still verify.", "danger"],
                ["Operational controls must contain the incident.", "warning"]
            ]
        },
        phishing: {
            title: "Credential Phishing",
            risk: "Medium",
            defense: "No password entry and server-side challenge issuance",
            summary: "Traditional password phishing becomes less useful because the user is not entering a reusable password. The phishing site would need both the browser-held device secret and a live challenge flow.",
            gridCaption: "Phishing pressure shifts from stealing passwords to stealing device context or proxying a live session.",
            grid: [
                ["Victim", "Fake page", "warning"],
                ["Phish site", "Requests login", "attack"],
                ["No password", "Nothing reusable", "defense"],
                ["Device secret", "Local only", "defense active"],
                ["Verifier", "Needs real proof", "focus defense"],
                ["Proxy risk", "Still possible", "warning"],
                ["Brand trust", "Needs UX cues", "trace"],
                ["Attacker", "Tries proxy", "attack"],
                ["Outcome", "Harder to steal", "defense"]
            ],
            attackerMoves: [
                "Send the user to a fake login page.",
                "Try to coerce entry of credentials or trigger a fake auth flow.",
                "Attempt to proxy a real backend challenge through the fake page."
            ],
            systemResponse: [
                "The browser uses a locally stored secret instead of manual password entry.",
                "The attacker still needs the device secret to sign the challenge correctly.",
                "Brand and origin checks remain important because live proxy phishing is still possible."
            ],
            timeline: [
                ["Victim lands on a fake login page.", "warning"],
                ["No reusable password is available to steal directly.", "success"],
                ["Attacker cannot generate a valid signature without the local secret.", "success"],
                ["Origin awareness still matters for advanced proxy attacks.", "warning"]
            ]
        },
        quantum: {
            title: "Quantum Threat Outlook",
            risk: "Long-term strategic",
            defense: "Migration planning and crypto agility",
            summary: "This demo currently uses SHA-256-derived identities and challenge signing logic for clarity. The attack lab highlights that true long-term quantum resilience needs crypto agility, migration planning, and stronger post-quantum primitives in production.",
            gridCaption: "This view is strategic rather than immediate: the focus is on long-term migration readiness across the architecture.",
            grid: [
                ["Today", "Classical stack", "trace"],
                ["Future risk", "Quantum pressure", "warning"],
                ["Identity layer", "Needs agility", "focus"],
                ["Signing flow", "Upgradeable", "defense"],
                ["Enrollment", "Migration path", "defense active"],
                ["Backend", "Replace primitives", "trace"],
                ["Users", "Operational change", "warning"],
                ["Roadmap", "Plan early", "defense"],
                ["Outcome", "Resilient system", "success"]
            ],
            attackerMoves: [
                "Target ecosystems that depend on long-lived classical assumptions.",
                "Wait for practical quantum advantages against legacy cryptography.",
                "Exploit systems that cannot rotate or upgrade their trust model."
            ],
            systemResponse: [
                "Keep identity and signing layers replaceable rather than hard-coded.",
                "Design user and device enrollment so upgrades are operationally realistic.",
                "Treat this prototype as an educational bridge, not a final PQC implementation."
            ],
            timeline: [
                ["Threat modeling starts years before the attack becomes practical.", "warning"],
                ["Systems with crypto agility can swap primitives over time.", "success"],
                ["Rigid systems accumulate long-term migration risk.", "danger"],
                ["Operational readiness is as important as algorithm choice.", "success"]
            ]
        }
    };

    const titleEl = document.getElementById("scenarioTitle");
    const riskEl = document.getElementById("scenarioRisk");
    const defenseEl = document.getElementById("scenarioDefense");
    const summaryEl = document.getElementById("scenarioSummary");
    const attackerMovesEl = document.getElementById("attackerMoves");
    const systemResponseEl = document.getElementById("systemResponse");
    const timelineEl = document.getElementById("simulationTimeline");
    const progressEl = document.getElementById("scenarioProgress");
    const prevButton = document.getElementById("prevScenario");
    const nextButton = document.getElementById("nextScenario");
    const pulseCells = Array.from(document.querySelectorAll(".pulse-cell"));
    const gridCaptionEl = document.getElementById("gridCaption");
    const scenarioKeys = Object.keys(scenarios);
    let currentIndex = 0;

    function renderList(element, items) {
        element.innerHTML = "";
        items.forEach(function (item) {
            const li = document.createElement("li");
            li.textContent = item;
            element.appendChild(li);
        });
    }

    function renderTimeline(items) {
        timelineEl.innerHTML = "";
        items.forEach(function (item) {
            const div = document.createElement("div");
            div.className = `timeline-item ${item[1]}`;
            div.innerHTML = `<strong>${item[0]}</strong>`;
            timelineEl.appendChild(div);
        });
    }

    function renderGrid(items) {
        pulseCells.forEach(function (cell, index) {
            const item = items[index] || ["", "", ""];
            cell.className = "pulse-cell";
            String(item[2] || "").split(" ").filter(Boolean).forEach(function (name) {
                cell.classList.add(name);
            });
            cell.innerHTML = `<small>${item[0]}</small><strong>${item[1]}</strong>`;
        });
    }

    function renderScenario(key) {
        const scenario = scenarios[key];
        if (!scenario) {
            return;
        }

        currentIndex = scenarioKeys.indexOf(key);
        titleEl.textContent = scenario.title;
        riskEl.textContent = scenario.risk;
        defenseEl.textContent = scenario.defense;
        summaryEl.textContent = scenario.summary;
        progressEl.textContent = `${currentIndex + 1} / ${scenarioKeys.length}`;
        gridCaptionEl.textContent = scenario.gridCaption || "";
        renderList(attackerMovesEl, scenario.attackerMoves);
        renderList(systemResponseEl, scenario.systemResponse);
        renderTimeline(scenario.timeline);
        renderGrid(scenario.grid || []);

        document.querySelectorAll(".scenario-button").forEach(function (button) {
            button.classList.toggle("is-active", button.dataset.scenario === key);
        });
    }

    document.querySelectorAll(".scenario-button").forEach(function (button) {
        button.addEventListener("click", function () {
            renderScenario(button.dataset.scenario);
        });
    });

    prevButton.addEventListener("click", function () {
        const nextIndex = (currentIndex - 1 + scenarioKeys.length) % scenarioKeys.length;
        renderScenario(scenarioKeys[nextIndex]);
    });

    nextButton.addEventListener("click", function () {
        const nextIndex = (currentIndex + 1) % scenarioKeys.length;
        renderScenario(scenarioKeys[nextIndex]);
    });

    wireExternalSiteLinks();
    renderScenario("replay");
})();
