/*
----------------------------------------------------------
App.jsx

Purpose
-------
Main Dashboard of Mini LLM

Responsibilities

1. Display Header
2. Display Welcome Section
3. Display Prompt Card
4. Display Output Card
5. Call FastAPI
6. Display Feature Cards
7. Display Footer
----------------------------------------------------------
*/

import { useState } from "react";

import "./App.css";

import Header from "./components/Header";
import PromptBox from "./components/PromptBox";
import OutputBox from "./components/OutputBox";

import { generateText } from "./services/api";

function App() {

    // Stores AI Response
    const [output, setOutput] = useState("");

    // Loading State
    const [loading, setLoading] = useState(false);

    // Generate Button Click
    const handleGenerate = async (prompt) => {

        setLoading(true);

        try {

            const result = await generateText(prompt);

            setOutput(result);

        } catch (error) {

            console.error(error);

            setOutput("Unable to connect to the server.");

        }

        setLoading(false);

    };

    return (

        <div className="container">

            {/* Header */}

            <Header />

            {/* Hero Section */}

            <section className="hero">

                <h2>

                    ✨ Welcome to Mini LLM ✨

                </h2>

                <p>

                    Enter your prompt and let AI generate
                    human-like text for you.

                </p>

            </section>

            {/* Main Content */}

            <section className="content">

                <div className="card">

                    <PromptBox

                        onGenerate={handleGenerate}

                        loading={loading}

                    />

                </div>

                <div className="card">

                    <OutputBox

                        output={output}

                        loading={loading}

                    />

                </div>

            </section>

            {/* Features */}

            <section className="features">

                <div className="feature">

                    <h3>⚡ Lightning Fast</h3>

                    <p>

                        Generate responses within seconds.

                    </p>

                </div>

                <div className="feature">

                    <h3>🔒 Secure</h3>

                    <p>

                        Your prompts stay private.

                    </p>

                </div>

                <div className="feature">

                    <h3>🧠 Smart AI</h3>

                    <p>

                        Powered by our Mini LLM model.

                    </p>

                </div>

                <div className="feature">

                    <h3>🚀 Modern Stack</h3>

                    <p>

                        Built with React, FastAPI & PyTorch.

                    </p>

                </div>

            </section>

            {/* Footer */}

            <footer className="footer">

                © 2026 <strong>VPro Skills</strong>

                <br />

                Mini LLM Project using React + FastAPI + PyTorch

            </footer>

        </div>

    );

}

export default App;