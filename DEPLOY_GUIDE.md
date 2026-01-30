# 🚀 Deployment Guide: Flask Backend

Required files have been added:
-   `Procfile`: Tells Render how to start the app.
-   `.gitignore`: Prevents secrets (.env) from being uploaded.
-   `requirements.txt`: Added `gunicorn` for production server.

---

## Part 1: Push to GitHub

1.  **Initialize Git** (if not done):
    ```bash
    cd c:/fix-back/flask_backend
    git init
    git add .
    git commit -m "Initial commit for Flask Backend"
    ```

2.  **Create Repo on GitHub**:
    -   Go to GitHub -> New Repository.
    -   Name it `pos-flask-backend` (or similar).

3.  **Link and Push**:
    *(Replace `YOUR_GITHUB_URL` with the one from the previous step)*
    ```bash
    git branch -M main
    git remote add origin YOUR_GITHUB_URL
    git push -u origin main
    ```

---

## Part 2: Deploy on Render

1.  **Create Service**:
    -   Log in to [Render Dashboard](https://dashboard.render.com).
    -   Click **New +** -> **Web Service**.
    -   Connect your GitHub repository.

2.  **Configure Settings**:
    -   **Name**: `pos-flask-backend`
    -   **Runtime**: Python 3
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `gunicorn run:app` (Render might auto-detect this from Procfile).

3.  **Environment Variables (Critical!)**:
    -   Click **"Advanced"** or **"Environment"**.
    -   Add the keys from your local `.env` file:
        -   `DB_HOST`: (Your Production Host, likely `shuttle.proxy.rlwy.net`)
        -   `DB_PORT`: (e.g. `40214`)
        -   `DB_USER`: `root`
        -   `DB_PASSWORD`: (Your Production Password)
        -   `DB_NAME`: `testdb`
        -   `ACCESS_TOKEN_SECRET`: (MUST match the Node.js one)
        -   `JWT_ALGORITHM`: `HS256`

4.  **Deploy**:
    -   Click **Create Web Service**.
    -   Wait for the build to finish.
    -   Your URL will be something like `https://pos-flask-backend.onrender.com`.

---

## Part 3: Connect Node.js
If your Node.js backend is running elsewhere (also on Render?), ensure they both point to the **Same Database** and share the **Same Secret**.
