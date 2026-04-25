# Deployment Guide

## Backend

Deploy `backend/` to Render.

Use:

- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`

Set environment variables:

- `EMAIL_USER`
- `EMAIL_PASS`

## Frontends

Deploy these as separate static sites:

1. `fintech-frontend/`
2. `demo-frontend/`
3. `attack-simulations/`

For `fintech-frontend/config.js` and `demo-frontend/config.js`, set:

```js
window.BACKEND_URL = "https://your-render-backend.onrender.com";
```

The attack simulation website is static and does not require backend configuration.
