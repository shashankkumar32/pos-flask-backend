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

## 📦 Preparing for Zip (Cleanup)

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
