# 🔐 Quantum Auth System

## 🚀 Project Overview

This project implements a **password-less authentication system** using **digital signatures**, designed to be **future-ready for post-quantum cryptography**.

Instead of passwords, users prove their identity by **signing a server-generated challenge**.

---

# 🧠 Core Idea

### Traditional Authentication:

* User → enters password → server verifies

### Our System:

* Server → sends challenge
* User → signs challenge
* Server → verifies signature

👉 No passwords
👉 Based on cryptography

---

# 🎯 Problem Statement

Modern systems rely on:

* Passwords
* Classical cryptography (RSA, ECC)

These are vulnerable to:

* Data breaches
* Quantum attacks (e.g., Shor’s Algorithm)

---

# 💡 Solution

We built a **challenge-response authentication system** using digital signatures.

---

# 🏗️ System Architecture

## 🔐 Backend (Security Layer)

Handles:

* Key generation
* Signing
* Verification
* API endpoints

---

## 🎨 Frontend (User Layer)

Handles:

* User input
* API communication
* Display results

---

## 📁 Storage

* Temporary (in-memory / JSON)
* Stores:

  * username
  * public key
  * secret key (demo only)

---

## 🔗 Communication

Frontend ↔ Backend via REST APIs

---

# 🔁 Complete System Workflow

## 🧩 1. Registration

User → enters username
Frontend → sends:

POST /register

Backend:

* Generates keypair
* Stores user

Response:

```json id="readmejson1"
{
  "message": "User registered successfully"
}
```

---

## 🧩 2. Login (Challenge Generation)

Frontend sends:

POST /login

Backend:

* Checks user
* Generates challenge

Response:

```json id="readmejson2"
{
  "challenge": "hex_string"
}
```

---

## 🧩 3. Signing

Challenge is signed using secret key:

signature = Sign(challenge, secret_key)

---

## 🧩 4. Verification

Frontend sends:

POST /verify

```json id="readmejson3"
{
  "username": "user1",
  "message": "challenge",
  "signature": "signature"
}
```

Backend:

* Fetches public key
* Verifies signature

---

## 🧠 Result

✅ Success:

```json id="readmejson4"
{
  "status": "success"
}
```

❌ Failure:

```json id="readmejson5"
{
  "status": "failed"
}
```

---

# 👤 User Flow

1. User opens app
2. Registers
3. Logs in
4. Receives challenge
5. System signs & verifies
6. Sees result

---

# 🧠 Core Security Concepts

* Authentication
* Public Key Cryptography
* Digital Signatures
* Challenge-Response Mechanism
* Post-Quantum Security (conceptual)

---

# ⚙️ Backend Implementation

## Tech Stack

* Python
* Flask
* PyNaCl (Ed25519 signatures)

---

## API Endpoints

### POST /register

Registers user and generates keys

---

### POST /login

Generates authentication challenge

---

### POST /verify

Verifies signed challenge

---

## Run Backend

```bash id="readmecmd1"
pip install flask pynacl
python app.py
```

Server:

```plaintext id="readmecmd2"
http://127.0.0.1:5000
```

---

# 🧪 Testing Flow

1. Register
2. Login
3. Verify

---

# ⚠️ Limitations

* Secret key stored on server (demo only)
* No database
* No frontend yet
* PQC not fully implemented

---

# 🚀 Future Enhancements

* Replace Ed25519 with:

  * CRYSTALS-Dilithium
  * Falcon
* Move signing to client-side
* Add frontend UI
* Add database
* Add blockchain layer

---

# 🏁 Hackathon Goal

Build a working prototype of:

> A quantum-ready, password-less authentication system

---

# 👥 Team Workflow

## Git Setup

### Initial Setup

```bash id="git1"
git clone <repo>
git checkout -b feature-yourname
```

### Daily Workflow

```bash id="git2"
git pull origin main
git add .
git commit -m "update"
git push origin feature-yourname
```

---

# 👨‍💻 Backend Team Plan

See detailed execution:
👉 

---

# 🎨 Frontend Team Plan

See detailed execution:
👉 

---

# 📊 Current Status

✅ Backend working
⏳ Frontend pending
⏳ Client-side signing pending

---

# 🎤 One-Line Pitch

> “We built a password-less authentication system where users prove identity by signing a challenge using quantum-safe cryptography.”

---

# 🔥 Success Criteria

✅ User can:

* Register
* Login
* Authenticate

👉 Without password
👉 Using cryptographic signatures

---
