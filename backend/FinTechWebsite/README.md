# QuantumPay Full-Stack Project

QuantumPay is a deployable full-stack system made of three coordinated parts:

- `backend/` - Flask authentication service with blockchain simulation, SQLite user storage, email delivery, and Flask-SocketIO event emission
- `fintech-frontend/` - user-facing fintech website
- `demo-frontend/` - real-time visualization dashboard powered by WebSockets

## Directory Structure

```text
FinTechWebsite/
├── backend/
│   ├── app.py
│   ├── socket_events.py
│   ├── blockchain/
│   │   └── chain.py
│   ├── crypto/
│   │   └── pqc.py
│   ├── storage/
│   │   └── db.py
│   ├── mailer/
│   │   └── email_service.py
│   ├── config/
│   │   └── config.py
│   ├── requirements.txt
│   ├── Procfile
│   └── runtime.txt
├── fintech-frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── styles.css
│   └── app.js
├── demo-frontend/
│   ├── index.html
│   ├── demo.js
│   └── demo.css
├── PROJECT_CONTEXT_PROMPT.md
└── README.md
```

## System Flow

### Register

1. User registers on `fintech-frontend/register.html`
2. Backend generates:
   - `secret_key`
   - `public_key = SHA256(secret_key)`
3. Backend stores user data in SQLite
4. Backend stores public identity in the blockchain simulation
5. Backend sends the secret key by email
6. Backend emits:
   - `key_generated`

### Login

1. User logs in on `fintech-frontend/login.html`
2. Backend creates a challenge
3. Backend emits:
   - `challenge_created`
4. Fintech frontend generates the signature using CryptoJS
5. Backend receives the signature and emits:
   - `signature_generated`

### Verify

1. Backend verifies the signature against the stored in-memory secret key
2. Backend emits one of:
   - `auth_success`
   - `auth_failed`
3. Demo frontend updates live through Socket.IO

## Backend Stack

- Flask
- Flask-Cors
- Flask-SocketIO
- eventlet
- SQLite
- Gmail SMTP

## Local Setup

### 1. Backend

From `FinTechWebsite/backend/`:

```bash
pip install -r requirements.txt
```

Set environment variables:

```bash
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASS=your_gmail_app_password
```

On PowerShell:

```powershell
$env:EMAIL_USER="your_gmail_address@gmail.com"
$env:EMAIL_PASS="your_gmail_app_password"
```

Run the backend:

```bash
python app.py
```

Local backend URL:

```text
http://127.0.0.1:5000
```

### 2. FinTech Frontend

From `FinTechWebsite/fintech-frontend/`:

```bash
python -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

### 3. Demo Frontend

From `FinTechWebsite/demo-frontend/`:

```bash
python -m http.server 5600
```

Open:

```text
http://127.0.0.1:5600
```

## Backend Events

Socket.IO events emitted by the backend:

- `key_generated`
- `challenge_created`
- `signature_generated`
- `auth_success`
- `auth_failed`

## Production Configuration

Do not use localhost in production.

Both frontends support overriding the backend URL with a global value before loading the app scripts:

```html
<script>
  window.BACKEND_URL = "https://your-backend.onrender.com";
</script>
```

## Render Deployment

Deploy `FinTechWebsite/backend/` as the backend service.

Included files:

- `requirements.txt`
- `Procfile`
- `runtime.txt`

Render environment variables:

- `EMAIL_USER`
- `EMAIL_PASS`

Backend start command is already defined in `Procfile`:

```text
web: python app.py
```

## Netlify Deployment

Deploy these as separate static sites:

1. `FinTechWebsite/fintech-frontend/`
2. `FinTechWebsite/demo-frontend/`

Before deployment, set:

```html
<script>
  window.BACKEND_URL = "https://your-backend.onrender.com";
</script>
```

in both frontends if needed, or inject it via Netlify snippet/template.

## Testing the Real-Time System

1. Open the demo frontend
2. Open the fintech frontend
3. Register a user
4. Observe `key_generated` in the demo UI
5. Login as the user
6. Observe:
   - `challenge_created`
   - `signature_generated`
   - `auth_success` or `auth_failed`

## Notes

- The original project outside `FinTechWebsite/` was left untouched.
- The blockchain is a simulation for identity visualization and auditability.
- SQLite stores user records.
- Secret keys are still stored in backend memory for verification, matching the existing project constraints.
- `PROJECT_CONTEXT_PROMPT.md` contains a single-share explanation you can paste into another AI chat.
