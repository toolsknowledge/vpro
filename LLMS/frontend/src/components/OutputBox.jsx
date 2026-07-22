/*
----------------------------------------------------------
OutputBox.jsx

Purpose
-------
Display the AI generated response.

Responsibilities

1. Show Loading State
2. Show AI Response
3. Copy Response
4. Download Response
5. Empty State
----------------------------------------------------------
*/

function OutputBox({ output, loading }) {

    // Copy Response
    const handleCopy = async () => {

        if (!output) return;

        try {

            await navigator.clipboard.writeText(output);

            alert("Response copied successfully!");

        } catch (error) {

            console.error(error);

        }

    };

    // Download Response
    const handleDownload = () => {

        if (!output) return;

        const blob = new Blob(

            [output],

            { type: "text/plain" }

        );

        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;

        link.download = "mini-llm-response.txt";

        link.click();

        URL.revokeObjectURL(url);

    };

    return (

        <>

            <h2>

                🤖 AI Generated Response

            </h2>

            <p>

                Your generated response will appear below.

            </p>

            <div className="output-box">

                {

                    loading

                    ?

                    <div className="loading">

                        ⏳ Generating response...

                    </div>

                    :

                    output

                    ?

                    output

                    :

                    <div className="empty-state">

                        🚀 Your AI response will appear here.

                    </div>

                }

            </div>

            <div className="button-group">

                <button

                    className="copy-btn"

                    onClick={handleCopy}

                    disabled={!output}

                >

                    📋 Copy

                </button>

                <button

                    className="download-btn"

                    onClick={handleDownload}

                    disabled={!output}

                >

                    💾 Download

                </button>

            </div>

        </>

    );

}

export default OutputBox;