# Flask Backend API Documentation (CURL)

This document provides a list of all available API endpoints in the Flask backend, along with example `curl` commands.

**Base URL:** `http://localhost:5000`

---

## 🔐 Authentication APIs

### 1. Electron Signin (Machine ID Tracking)
*Note: This endpoint tracks the machine from which the user is logging in.*

```bash
curl -X POST http://localhost:5000/api/auth/electron/signin \
-H "Content-Type: application/json" \
-d '{
  "username": "john@example.com",
  "password": "password123",
  "machineId": "MACHINE_UID_12345"
}'
```

---

## 📦 Order Synchronization APIs
*Requires Header: `Authorization: Bearer <TOKEN>`*

### 1. Bulk Create Orders (Sync from Local POS)
*This endpoint accepts an array of orders to sync from the local terminal to the cloud vault.*

```bash
curl -X POST http://localhost:5000/api/orders/bulk \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '[
  {
    "totalAmount": 1250,
    "customerName": "John Doe",
    "customerPhone": "9876543210",
    "tableNumber": "12",
    "invoiceId": "INV-001",
    "paymentMethod": "UPI",
    "status": "PAID",
    "date": "2024-03-20T10:00:00Z",
    "items": [
      { "name": "Chicken Curry", "quantity": 1, "price": 450 },
      { "name": "Naan", "quantity": 2, "price": 40 }
    ]
  }
]'
```

---

## 🛠️ Security & Headers
- **Content-Type**: All POST requests must include `Content-Type: application/json`.
- **Authorization**: Protected routes require a Bearer token in the `Authorization` header.
- **Port**: Defaults to `5000` but can be configured via `FLASK_APP_PORT` in `.env`.
