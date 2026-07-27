/*
-------------------------------------------------------
PromptBox.jsx

Purpose
-------
Accept user prompt and send it to App.jsx

Responsibilities

1. Accept user input
2. Validate prompt
3. Clear prompt
4. Character Counter
5. Generate Button
6. Loading State
7. Ctrl + Enter Support
-------------------------------------------------------
*/

import { useState } from "react";

function PromptBox({ onGenerate, loading }) {

    const [prompt, setPrompt] = useState("");

    // Generate Button Click
    const handleGenerate = () => {

        if (prompt.trim() === "") {

            alert("Please enter a prompt.");

            return;

        }

        onGenerate(prompt);

    };

    // Clear Prompt
    const handleClear = () => {

        setPrompt("");

    };

    // Ctrl + Enter Shortcut
    const handleKeyDown = (event) => {

        if (event.ctrlKey && event.key === "Enter") {

            handleGenerate();

        }

    };

    return (

        <>

            <h2>

                ✍️ Enter Your Prompt

            </h2>

            <p>

                Describe what you want the AI to generate.

            </p>

            <textarea

                placeholder="Example: Explain Python for beginners in simple words..."

                value={prompt}

                onChange={(e) => setPrompt(e.target.value)}

                onKeyDown={handleKeyDown}

                maxLength={1000}

            />

            <div className="prompt-footer">

                <span className="counter">

                    {prompt.length} / 1000 Characters

                </span>

                <div className="button-group">

                    <button

                        className="clear-btn"

                        onClick={handleClear}

                    >

                        Clear

                    </button>

                    <button

                        className="generate-btn"

                        onClick={handleGenerate}

                        disabled={loading}

                    >

                        {

                            loading

                            ?

                            "Generating..."

                            :

                            "🚀 Generate"

                        }

                    </button>

                </div>

            </div>

            <div className="tip">

                💡 Tip: Press <strong>Ctrl + Enter</strong> to generate instantly.

            </div>

        </>

    );

}

export default PromptBox;