/*
----------------------------------------
main.jsx

Purpose
-------
Entry point of the React application.

Responsibilities

1. Start React
2. Load App Component
3. Attach React to HTML
----------------------------------------
*/

import React from "react";

import ReactDOM from "react-dom/client";

import App from "./App";

import "./App.css";

ReactDOM.createRoot(

    document.getElementById("root")

).render(

    <React.StrictMode>

        <App />

    </React.StrictMode>

);