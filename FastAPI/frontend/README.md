# VPro Skills · Student Portal (React)

React + Vite frontend for the FastAPI student API in `../FastAPI`, secured with JWT.

## Run

```bash
# 1. Start FastAPI (from ../FastAPI)
uvicorn main:app --reload          # http://127.0.0.1:8000

# 2. Start React (from this folder)
npm install
npm run dev                        # http://localhost:5173
```

The Vite dev server proxies `/api/*` to FastAPI, so the backend needs no CORS setup.
Copy `.env.example` to `.env` to point at a different API host.

## Features

- Register / sign in. The JWT is stored in `localStorage` and sent as `Authorization: Bearer <token>`.
- Session countdown in the header, with automatic sign-out when the token expires or the API returns 401/403.
- Student dashboard: stats, course filter chips, search, sortable columns, add/edit/delete in modals.
- Responsive: table on desktop, cards, a floating add button and bottom-sheet modals on mobile.

## Structure

```
src/
  api/client.js            fetch wrapper, token storage, API calls
  context/AuthContext.jsx  login/register/logout, JWT decode, auto-expiry
  context/ToastContext.jsx notifications
  components/              Header, Modal, StudentForm, route guards
  pages/AuthPage.jsx       sign in + register
  pages/Dashboard.jsx      student management
```

## Production

`npm run build` outputs `dist/`. When the frontend is served from a different origin than the API,
set `VITE_API_URL` and add `CORSMiddleware` to FastAPI.
