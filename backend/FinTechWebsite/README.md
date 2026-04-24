# QuantumPay FinTechWebsite

QuantumPay is now a self-contained fintech demo application inside `FinTechWebsite/`, with its own backend and frontend while leaving the original project outside it untouched.

## Structure

```text
FinTechWebsite/
├── backend/
│   ├── app.py
│   ├── blockchain/
│   │   └── chain.py
│   ├── crypto/
│   │   └── pqc.py
│   ├── storage/
│   │   └── db.py
│   ├── mailer/
│   │   └── email_service.py
│   └── config/
│       └── config.py
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── styles.css
│   └── app.js
├── PROJECT_CONTEXT_PROMPT.md
├── requirements.txt
└── README.md
```

## Features

- Dedicated Flask backend on port `5001`
- User data stored in SQLite
- Public keys stored in a blockchain simulation
- Secret keys generated during registration and emailed with Gmail SMTP
- Trusted-device frontend flow that avoids manual secret entry on every login
- PhonePe-inspired purple fintech frontend
- One-file AI context prompt for reuse in any chat assistant

## Prerequisites

- Python 3.10+
- Gmail account with an app password

## Environment Variables

Set these before starting the backend:

```bash
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASS=your_gmail_app_password
```

On PowerShell:

```powershell
$env:EMAIL_USER="your_gmail_address@gmail.com"
$env:EMAIL_PASS="your_gmail_app_password"
```

## Local Setup

1. Install the FinTechWebsite Python dependencies:

```bash
pip install -r requirements.txt
```

2. Start the FinTechWebsite backend:

```bash
python backend/app.py
```

3. Serve the frontend:

```bash
cd frontend
python -m http.server 5500
```

4. Open:

```text
http://127.0.0.1:5500
```

## Gmail Setup

1. Enable 2-Step Verification on your Gmail account.
2. Generate an App Password in Google Account security settings.
3. Use that app password as `EMAIL_PASS`.
4. Use your Gmail address as `EMAIL_USER`.

## Registration Flow

1. User submits name, email, phone, and username.
2. Frontend calls `POST http://127.0.0.1:5001/register`.
3. FinTechWebsite backend generates:
   - `secret_key`
   - `public_key = SHA256(secret_key)`
4. User profile is stored in SQLite.
5. Public key is written into the blockchain simulation.
6. Secret key is emailed to the user.
7. Frontend silently stores the returned device credential locally for trusted-device sign-in.

## Login Flow

1. User enters username only.
2. Frontend loads the locally stored device credential for that username.
3. Frontend calls `POST /login` on the FinTechWebsite backend.
4. Backend returns a challenge.
5. Frontend computes:

```text
signature = SHA256(challenge + secret_key)
```

6. Frontend submits the signature to `POST /verify`.
7. On success, the user is redirected to the dashboard.

## Security Notes

- The secret key is never rendered on the page.
- User profile data lives in SQLite.
- Public identity data lives in the blockchain simulation.
- Secret keys are retained in backend memory for verification and replay-safe challenge handling.
- Challenges are consumed after verification attempts.
- Errors from the backend are surfaced cleanly in the UI.

## Deployment Prep

### Backend service

- Deploy `FinTechWebsite/backend/app.py` to Render.
- Configure `EMAIL_USER` and `EMAIL_PASS` in Render environment variables.
- Ensure the backend exposes:
  - `/register`
  - `/login`
  - `/verify`
  - `/status`
  - `/blockchain`

### Frontend

- Deploy `frontend/` to Netlify.
- If your deployed backend runs on a different URL, set this global before loading `app.js`:

```html
<script>
  window.AUTH_API_BASE = "https://your-fintech-backend.onrender.com";
</script>
```

## Notes

- The original project backend and frontend outside `FinTechWebsite/` remain untouched.
- The FinTechWebsite backend is self-contained and independent.
- Use `PROJECT_CONTEXT_PROMPT.md` when you want to explain the whole project to another AI in one paste.
