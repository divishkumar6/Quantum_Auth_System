# QuantumPay Deployment Guide

## Backend on Render

Service root directory:

`backend/FinTechWebsite/backend`

Required files already present:

- `requirements.txt`
- `Procfile`
- `runtime.txt`

Runtime env vars:

- `EMAIL_USER`
- `EMAIL_PASS`

Start command:

`python app.py`

Build command:

`pip install -r requirements.txt`

## Frontends on Netlify

Deploy these as two separate static sites:

1. `backend/FinTechWebsite/fintech-frontend`
2. `backend/FinTechWebsite/demo-frontend`

Before deploying, update:

- `fintech-frontend/config.js`
- `demo-frontend/config.js`

Set both to your Render backend URL:

```js
window.BACKEND_URL = "https://your-render-service.onrender.com";
```

## Important production notes

- The backend already enables CORS with `cors_allowed_origins="*"`.
- Socket.IO is started with `socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))`.
- Do not leave any `127.0.0.1` references in deployed frontend files.
- SQLite storage in this project is local-file based. On many cloud platforms, local disk can be ephemeral, so production user data may not persist reliably across redeploys or restarts.
