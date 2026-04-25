# QuantumPay Platform

QuantumPay is now organized as one backend service plus three separate static websites:

- `backend/` - Flask + Socket.IO authentication backend
- `fintech-frontend/` - customer-facing fintech website
- `demo-frontend/` - realtime backend process demo
- `attack-simulations/` - interactive security and attack simulation website

## Local Run

Backend:

```powershell
cd backend
pip install -r requirements.txt
python app.py
```

Fintech frontend:

```powershell
cd fintech-frontend
python -m http.server 5500
```

Demo frontend:

```powershell
cd demo-frontend
python -m http.server 5600
```

Attack simulations:

```powershell
cd attack-simulations
python -m http.server 5700
```

## Deployment Targets

- Render: `backend/`
- Netlify site 1: `fintech-frontend/`
- Netlify site 2: `demo-frontend/`
- Netlify site 3: `attack-simulations/`

Update these before deploying:

- `fintech-frontend/config.js`
- `demo-frontend/config.js`

Set both to your deployed Render backend URL.
