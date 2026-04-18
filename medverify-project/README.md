# MedVerify Frontend

A pure HTML/CSS/JS frontend — no build step required.

## Files

- `index.html` — App shell and all HTML markup
- `style.css`  — Full dark theme styles
- `app.js`     — All logic: auth, file upload, API calls, rendering

## Setup

1. Open `app.js` and set the backend URL on line 2:
   ```js
   const API_BASE = "http://localhost:8000"; // or your deployed backend URL
   ```

2. Open `index.html` directly in a browser **or** serve it with any static server:
   ```bash
   # Python
   python -m http.server 3000

   # Node (npx)
   npx serve .
   ```

3. Navigate to `http://localhost:3000`

## Demo Credentials
| Email                    | Password       |
|--------------------------|----------------|
| faculty@hospital.com     | medverify2025  |
| admin@medverify.com      | admin123       |
