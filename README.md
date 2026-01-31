# Flask Bulk Order Backend

This microservice handles high-volume bulk order processing for the POS system.

## 🚀 Setup & Run

### 1. Prerequisites
-   Python 3.8+ installed.
-   MySQL Database running (shared with Node.js backend).

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
Ensure the `.env` file is present in this directory with the following keys (copied from Node.js backend):
-   `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
-   `ACCESS_TOKEN_SECRET` (Must match Node.js secret)

### 4. Run the Server
```bash
python run.py
```
*Server runs on `http://localhost:5000` by default.*

---

## 🛠️ API Documentation

### POST `/api/orders/bulk`
Creates multiple orders in a single atomic transaction.

#### Updated Request Body (JSON Array)
Each object in the array now supports the following fields to match the Node.js backend:

| Field | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **`totalAmount`** | Number | Total price of the order | **Required** |
| **`customerName`** | String | Name of the customer | `"Bulk Customer"` |
| **`tableNumber`** | String | Table assigned to the order | `null` |
| **`customerPhone`** | String | Phone number | `null` |
| **`customerEmail`** | String | Email address | `null` |
| **`notes`** | String | Special instructions/notes | `null` |
| **`orderType`** | String | Type of order (e.g., DINE_IN) | `""` (Empty string) |
| **`status`** | String | Maps to `orderStatus` | `"WAITING"` |
| **`items`** | Array | List of items in the order | `[]` |

#### Final cURL Test Command
```bash
curl -X POST http://localhost:5000/api/orders/bulk \
  -H "Content-Type: application/json" \
  -H "x-access-token: YOUR_TOKEN_HERE" \
  -d '[
    {
      "customerName": "John Doe",
      "totalAmount": 150.00,
      "tableNumber": "T5",
      "customerPhone": "9876543210",
      "customerEmail": "john@example.com",
      "notes": "No spicy",
      "status": "pending",
      "items": [
        { "name": "Item A", "price": 100.00, "quantity": 1 },
        { "name": "Item B", "price": 50.00, "quantity": 1 }
      ]
    }
  ]'
```

---

## 📦 Preparing for Zip (Cleanup)
... (remainder of existing cleanup instructions)

If you need to zip this project (e.g., for sharing or deployment), **DELETE** the folders and files listed below to keep the file size small and secure.

### 🗑️ Delete these Folders:
1.  `__pycache__/` (Found in `app/` and root) - *Compiled Python files, safe to delete.*
2.  `venv/` or `.venv/` - *Virtual environment folder (if you created one).*
3.  `.pytest_cache/` - *Test cache (if present).*

### ⚠️ Security Warning:
-   **`.env` file**: Contains SENSITIVE passwords and secrets.
    -   **exclude** it if sharing with untrusted parties.
    -   **include** it only if sharing with your team/deployment server.

### 📝 Example Cleanup Command (Windows PowerShell)
```powershell
Remove-Item -Path "app/__pycache__" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "__pycache__" -Recurse -ErrorAction SilentlyContinue
```
