
# Deployment Guide for AI RAG Summarizer

This application is ready to be deployed to cloud platforms like **Render**, **Railway**, or **Heroku**.

## Prerequisites
1.  **GitHub Account**: Your code must be pushed to a GitHub repository.
2.  **MongoDB Atlas**: You are already using this! Ensure your IP Whitelist allows access from anywhere (`0.0.0.0/0`) since cloud servers have dynamic IPs.
3.  **Groq API Key**: Have your key ready.

## Option 1: Deploy on Render (Recommended)

1.  **Push Code to GitHub**:
    *   Initialize git: `git init`
    *   Add files: `git add .`
    *   Commit: `git commit -m "Initial commit"`
    *   Create a repo on GitHub and push.

2.  **Create Service on Render**:
    *   Go to [dashboard.render.com](https://dashboard.render.com).
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.

3.  **Configure Settings**:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4.  **Environment Variables**:
    *   Scroll down to "Environment Variables" and add these:
        *   `MONGO_URI`: (Your connection string from .env)
        *   `DB_NAME`: `ai_summarizer`
        *   `GROQ_API_KEY`: (Your key)
        *   `SECRET_KEY`: (Your secret key)
        *   `ALGORITHM`: `HS256`
        *   `PYTHON_VERSION`: `3.10.0` (Optional, helps ensure compatibility)

5.  **Deploy**:
    *   Click "Create Web Service". Render will build and deploy your app.

## Option 2: Deploy on Railway

1.  Login to [Railway.app](https://railway.app).
2.  Click **New Project** -> **Deploy from GitHub repo**.
3.  Select your repo.
4.  Go to **Variables** tab and add the same environment variables as above (`MONGO_URI`, `GROQ_API_KEY`, etc.).
5.  Railway usually auto-detects Python and the Procfile I just created.

## Option 3: Deploy on Heroku

1.  Install Heroku CLI.
2.  Login: `heroku login`
3.  Create app: `heroku create my-summarizer-app`
4.  Add env vars: `heroku config:set MONGO_URI=... GROQ_API_KEY=...`
5.  Push: `git push heroku master`

---

### Important Note on MongoDB Access
Since you are deploying to a public cloud, the "Allow Access from Anywhere (0.0.0.0/0)" setting in MongoDB Atlas Network Access is **required**, as Render/Railway change IPs frequently.
