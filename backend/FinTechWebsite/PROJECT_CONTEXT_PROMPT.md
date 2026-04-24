# QuantumPay One-Prompt Context

```text
I am working on a project named QuantumPay inside a folder called FinTechWebsite. It is a deployable full-stack system with three parts:

1. backend/ - Flask authentication backend with Flask-SocketIO
2. fintech-frontend/ - user-facing fintech website
3. demo-frontend/ - real-time visualization website

Directory structure:
- FinTechWebsite/backend/
  - app.py
  - socket_events.py
  - blockchain/chain.py
  - crypto/pqc.py
  - storage/db.py
  - mailer/email_service.py
  - config/config.py
  - requirements.txt
  - Procfile
  - runtime.txt
- FinTechWebsite/fintech-frontend/
  - index.html
  - register.html
  - login.html
  - dashboard.html
  - styles.css
  - app.js
- FinTechWebsite/demo-frontend/
  - index.html
  - demo.js
  - demo.css

Main goal:
- FinTech Website handles user interaction
- Backend handles registration, challenge generation, signature verification, email sending, blockchain simulation, SQLite storage, and Socket.IO events
- Demo Website visualizes the auth process in real time using WebSockets

Backend behavior:
- Registration:
  - accepts name, email, phone, username
  - generates secret_key
  - generates public_key = SHA256(secret_key)
  - stores user in SQLite
  - stores public key in blockchain simulation
  - stores users_secret[username] = secret_key in memory
  - sends secret key by Gmail SMTP using EMAIL_USER and EMAIL_PASS
  - emits `key_generated`
- Login:
  - accepts username
  - creates challenge
  - stores challenge in memory
  - emits `challenge_created`
- Verify:
  - accepts username, message, signature
  - emits `signature_generated` when signature is received
  - verifies signature = SHA256(challenge + secret_key)
  - removes the challenge after verification attempt
  - emits `auth_success` or `auth_failed`

Socket.IO event names:
- key_generated
- challenge_created
- signature_generated
- auth_success
- auth_failed

Backend routes:
- POST /register
- POST /login
- POST /verify
- GET /status
- GET /blockchain

Security model:
- Public keys live in blockchain simulation
- User profile data lives in SQLite
- Secret keys are sent by email and also retained in backend memory for verification
- Challenges are single-use to prevent replay attacks

Fintech frontend behavior:
- Register page posts to /register
- Login page posts to /login, then signs the challenge in the browser using CryptoJS, then posts to /verify
- It uses trusted-device local storage so users do not have to manually paste the secret key every time on the same browser
- Backend URL is configurable via window.BACKEND_URL

Demo frontend behavior:
- Uses Socket.IO CDN
- Connects to backend websocket endpoint
- Displays:
  - key panel
  - challenge panel
  - signature panel
  - result panel
  - timeline
- Uses animated typing and glow effects for live events

Deployment:
- Backend deploy target: Render
- Frontend deploy targets: Netlify
- Production should not use localhost
- Frontends should point to the deployed backend URL via window.BACKEND_URL

Environment variables:
- EMAIL_USER
- EMAIL_PASS

Current task types I need help with:
- debugging register/login/verify flow
- improving real-time demo behavior
- refining fintech frontend UI
- keeping Socket.IO, blockchain simulation, SQLite, and email delivery in sync
- preparing for deployment
```
