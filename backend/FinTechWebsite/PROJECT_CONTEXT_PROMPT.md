# QuantumPay Project Context Prompt

Use the following as a single prompt in any AI chat to explain this project clearly:

```text
I am working on a project called QuantumPay inside a folder named FinTechWebsite. It is a self-contained fintech demo application with the same high-level architecture style as the main project outside it: a backend folder and a frontend folder.

Project structure:
- FinTechWebsite/backend/
  - app.py
  - blockchain/chain.py
  - crypto/pqc.py
  - storage/db.py
  - mailer/email_service.py
  - config/config.py
- FinTechWebsite/frontend/
  - index.html
  - register.html
  - login.html
  - dashboard.html
  - styles.css
  - app.js

Core idea:
- The app simulates a secure fintech login system using challenge-response authentication.
- User profile data is stored in SQLite.
- Public identity data is stored in a blockchain simulation.
- Secret keys are generated during registration, stored temporarily in backend memory for verification, and mailed to the user.
- The browser also silently stores the returned device credential locally so the login page can work as a trusted-device experience without asking the user to manually paste the secret key every time.

Backend details:
- Flask app runs from FinTechWebsite/backend/app.py, default port 5001.
- Register endpoint:
  - accepts name, email, phone, username
  - generates secret_key
  - generates public_key = SHA256(secret_key)
  - stores user profile in SQLite
  - stores public_key in blockchain simulation
  - stores users_secret[username] = secret_key in memory
  - attempts to send the secret key by Gmail SMTP using EMAIL_USER and EMAIL_PASS
  - returns success plus email delivery status
- Login endpoint:
  - accepts username
  - creates a challenge
  - stores challenge in memory
  - returns challenge + public_key
- Verify endpoint:
  - accepts username, message, signature
  - checks challenge exists
  - checks message matches the stored challenge
  - loads secret key from in-memory users_secret
  - loads public key from blockchain simulation
  - computes expected_signature = SHA256(message + secret_key)
  - succeeds only when signature matches expected_signature
  - deletes the challenge after verification attempt to prevent replay attacks
- Additional endpoints:
  - /status
  - /blockchain

Security model:
- Challenge-response authentication
- Replay protection by deleting challenge after verification
- Tampered message detection
- Public key consistency check against blockchain simulation

Frontend details:
- Pure HTML/CSS/JS, no framework
- Visual design is a modern fintech style with a purple-led PhonePe-inspired direction
- Registration page:
  - sends name, email, phone, username to backend
  - if successful, silently stores secret_key in local browser storage as a trusted-device credential
  - shows backend status clearly if the backend is offline
- Login page:
  - asks only for username
  - fetches challenge from backend
  - loads locally stored device credential for that username
  - signs challenge using SHA256(challenge + secret_key) with CryptoJS
  - calls verify endpoint
  - redirects to dashboard on success
- Dashboard page:
  - static fintech-style wallet and transactions UI

Important constraints:
- The original project backend and frontend outside FinTechWebsite should remain untouched.
- FinTechWebsite is meant to be self-contained.
- The backend inside FinTechWebsite is separate from the main backend.
- Frontend should talk to the FinTechWebsite backend on port 5001 by default.

Environment requirements:
- Python with Flask and Flask-Cors
- Gmail SMTP credentials in environment variables:
  - EMAIL_USER
  - EMAIL_PASS

What I usually need help with:
- debugging registration, login, or verification issues
- improving the fintech UI and UX
- explaining the auth flow clearly
- deployment setup
- keeping the blockchain simulation, SQLite storage, and email delivery consistent
```
