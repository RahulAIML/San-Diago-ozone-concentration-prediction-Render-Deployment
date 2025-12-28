# Deployment Guide (Render)

The project is now configured for easy deployment on **Render**.

## 1. Prerequisites
*   Ensure your code is pushed to your **GitHub** repository.
*   Sign up for a [Render account](https://render.com/).

## 2. Deploying with Blueprints (Recommended)
This uses the `render.yaml` file I created to automatically set up both the Backend and Frontend.

1.  Go to the Render Dashboard.
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub repository.
4.  Render will detect `render.yaml`.
5.  Click **Apply**.
6.  Sit back! Render will build:
    *   **ozone-backend**: The Python Django API.
    *   **ozone-frontend**: The React static site.

## 3. Manual Deployment (If Blueprints fail)

### Backend (Web Service)
*   **Build Command**: `./build.sh`
*   **Start Command**: `cd django_backend && gunicorn ozone_api.wsgi:application`
*   **Environment Variables**:
    *   `PYTHON_VERSION`: `3.11.9`
    *   `SECRET_KEY`: (Generate a random string)
    *   `DEBUG`: `False`

### Frontend (Static Site)
*   **Build Command**: `npm install && npm run build`
*   **Publish Directory**: `dist`
*   **Environment Variables**:
    *   `VITE_API_URL`: The URL of your deployed backend (e.g., `https://ozone-backend.onrender.com`)

## 4. Important Notes
*   **Database**: This setup uses **SQLite**. On Render, the filesystem is ephemeral, meaning **database data will be lost** every time the server restarts or redeploys.
    *   To fix this in the future, you must switch to use a PostgreSQL database (Render provides a managed one).
*   **CORS**: `settings.py` is configured to allow all origins (`*`) for simplicity. In a real production environment, you should restrict this to your frontend domain.

## 5. Local Development
To run locally:
1.  **Backend**: `cd django_backend` -> `python manage.py runserver`
2.  **Frontend**: `cd frontend` -> `npm run dev`
