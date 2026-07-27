/*
--------------------------------------------------------
Header.jsx

Purpose
-------
Displays the application header.

Responsibilities

1. Display Company Logo
2. Display Application Name
3. Display Tagline
4. Display Technology Badge
--------------------------------------------------------
*/

import logo from "../assets/logo.jpeg";

function Header() {

    return (

        <header className="header">

            <div className="logo-section">

                <img
                    src={logo}
                    alt="VPro Skills Logo"
                    className="logo"
                />

                <div className="title-section">

                    <h1>

                        Mini LLM

                    </h1>

                    <p>

                        AI Powered Text Generator

                    </p>

                </div>

            </div>

            <div className="tech-badge">

                🚀 Built with FastAPI + React

            </div>

        </header>

    );

}

export default Header;