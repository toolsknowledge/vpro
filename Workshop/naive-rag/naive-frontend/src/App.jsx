import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [context, setContext] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // --------------------------------------------------
  // Upload PDF
  // --------------------------------------------------

  const uploadFile = async () => {
    if (!file) {
      setMessage("Please select a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setMessage("");
    setAnswer("");
    setContext([]);

    try {
      const response = await fetch(
        "http://localhost:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Upload failed.");
        return;
      }

      setMessage(
        `${data.message} • ${data.chunks} chunks created`
      );
    } catch (error) {
      setMessage(
        "Unable to connect to FastAPI. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };


  // --------------------------------------------------
  // Ask Question
  // --------------------------------------------------

  const askQuestion = async () => {
    if (!question.trim()) {
      setAnswer("Please enter a question.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setContext([]);

    try {
      const response = await fetch(
        `http://localhost:8000/ask?question=${encodeURIComponent(
          question
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setAnswer(data.detail || "Something went wrong.");
        return;
      }

      setAnswer(data.answer);
      setContext(data.context || []);
    } catch (error) {
      setAnswer(
        "Unable to connect to FastAPI. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };


  // --------------------------------------------------
  // Enter key
  // --------------------------------------------------

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };


  return (
    <div className="container">

      {/* =================================================
          HERO
      ================================================= */}

      <header
        style={{
          textAlign: "center",
          paddingTop: "35px",
          position: "relative",
        }}
      >

        <img
          src="/logo.jpeg"
          alt="VPro Skills"
          className="logo"
        />

        <h1 className="workshop-title">
          NAIVE RAG- WORKSHOP
        </h1>

        <p>
          Upload your document and ask anything about it.
        </p>

      </header>


      {/* =================================================
          MAIN SECTION
      ================================================= */}

      <main
        style={{
          maxWidth: "1100px",
          margin: "35px auto 0",
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "24px",
        }}
      >

        {/* =================================================
            UPLOAD CARD
        ================================================= */}

        <section
          className="card"
          style={{
            margin: 0,
            maxWidth: "none",
          }}
        >

          <div
            style={{
              width: "64px",
              height: "64px",
              margin: "0 auto 18px",
              borderRadius: "50%",
              background:
                "linear-gradient(135deg, #ff7900, #ff4b2b)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#fff",
              fontSize: "28px",
              boxShadow:
                "0 8px 20px rgba(255, 105, 0, 0.25)",
            }}
          >
            ↑
          </div>

          <h2>1. Upload Document</h2>

          <div
            style={{
              border: "2px dashed #ff8a1c",
              borderRadius: "14px",
              padding: "28px 20px",
              textAlign: "center",
              background: "#fffaf5",
            }}
          >

            <div
              style={{
                fontSize: "48px",
                marginBottom: "10px",
              }}
            >
              📄
            </div>

            <strong
              style={{
                display: "block",
                marginBottom: "8px",
              }}
            >
              Select your PDF document
            </strong>

            <span
              style={{
                display: "block",
                marginBottom: "15px",
                color: "#667085",
              }}
            >
              PDF files only
            </span>

            <input
              type="file"
              accept=".pdf"
              onChange={(event) =>
                setFile(event.target.files[0])
              }
            />

          </div>

          <button
            onClick={uploadFile}
            disabled={loading}
            style={{
              background:
                "linear-gradient(90deg, #071b34, #0b2948)",
            }}
          >
            {loading ? "Uploading..." : "↑  UPLOAD PDF"}
          </button>

          {file && (
            <div
              style={{
                marginTop: "15px",
                padding: "12px 15px",
                borderRadius: "10px",
                background: "#ecfdf3",
                color: "#16794c",
                fontSize: "14px",
              }}
            >
              ✓ Selected: {file.name}
            </div>
          )}

          {message && (
            <div
              style={{
                marginTop: "15px",
                padding: "12px 15px",
                borderRadius: "10px",
                background: "#eef6ff",
                color: "#175cd3",
                fontSize: "14px",
              }}
            >
              {message}
            </div>
          )}

        </section>


        {/* =================================================
            QUESTION CARD
        ================================================= */}

        <section
          className="card"
          style={{
            margin: 0,
            maxWidth: "none",
          }}
        >

          <div
            style={{
              width: "64px",
              height: "64px",
              margin: "0 auto 18px",
              borderRadius: "50%",
              background:
                "linear-gradient(135deg, #ff7900, #ff4b2b)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#fff",
              fontSize: "28px",
              fontWeight: "bold",
              boxShadow:
                "0 8px 20px rgba(255, 105, 0, 0.25)",
            }}
          >
            ?
          </div>

          <h2>2. Ask Question</h2>

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Type your question here..."
            style={{
              width: "100%",
              minHeight: "180px",
              padding: "18px",
              border: "1px solid #d6dce5",
              borderRadius: "12px",
              resize: "vertical",
              outline: "none",
              fontSize: "16px",
            }}
          />

          <button
            onClick={askQuestion}
            disabled={loading}
          >
            {loading ? "Thinking..." : "➤  ASK QUESTION"}
          </button>

          <div
            style={{
              marginTop: "15px",
              padding: "12px 15px",
              borderRadius: "10px",
              background: "#eef6ff",
              color: "#344054",
              fontSize: "14px",
            }}
          >
            💡 Upload a document first, then ask questions.
          </div>

        </section>

      </main>


      {/* =================================================
          ANSWER
      ================================================= */}

      <section
        className="card"
        style={{
          maxWidth: "1100px",
          marginTop: "25px",
        }}
      >

        <h2 style={{ textAlign: "left" }}>
          💬 Answer
        </h2>

        <div
          style={{
            minHeight: "170px",
            padding: "25px",
            borderRadius: "14px",
            background:
              "linear-gradient(135deg, #f7fbff, #eef6ff)",
            border: "1px solid #dce9f7",
          }}
        >

          {loading ? (

            <div
              style={{
                textAlign: "center",
                padding: "45px 10px",
                color: "#ff7900",
                fontWeight: "600",
              }}
            >
              Searching the document and generating answer...
            </div>

          ) : answer ? (

            <div>

              <p
                style={{
                  margin: 0,
                  whiteSpace: "pre-wrap",
                  lineHeight: "1.8",
                }}
              >
                {answer}
              </p>

            </div>

          ) : (

            <div
              style={{
                textAlign: "center",
                padding: "35px 10px",
                color: "#667085",
              }}
            >

              <div
                style={{
                  fontSize: "45px",
                  marginBottom: "10px",
                }}
              >
                🤖
              </div>

              <strong
                style={{
                  display: "block",
                  color: "#172033",
                  marginBottom: "5px",
                }}
              >
                Your answer will appear here
              </strong>

              <span>
                Ask a question to get started.
              </span>

            </div>

          )}

        </div>

      </section>


      {/* =================================================
          RETRIEVED CONTEXT
      ================================================= */}

      {context.length > 0 && (

        <section
          className="card"
          style={{
            maxWidth: "1100px",
            marginTop: "20px",
          }}
        >

          <h2 style={{ textAlign: "left" }}>
            🔎 Retrieved Context
          </h2>

          <div>

            {context.map((item, index) => (

              <div
                key={index}
                style={{
                  padding: "16px",
                  marginBottom: "12px",
                  borderRadius: "10px",
                  background: "#fafafa",
                  border: "1px solid #e4e7ec",
                  lineHeight: "1.7",
                  fontSize: "14px",
                }}
              >

                <strong
                  style={{
                    color: "#ff7900",
                  }}
                >
                  Chunk {index + 1}
                </strong>

                <p
                  style={{
                    marginBottom: 0,
                  }}
                >
                  {item}
                </p>

              </div>

            ))}

          </div>

        </section>

      )}


      {/* =================================================
          FEATURES
      ================================================= */}

      <section
        style={{
          maxWidth: "1100px",
          margin: "25px auto 0",
          display: "grid",
          gridTemplateColumns:
            "repeat(4, 1fr)",
          gap: "14px",
        }}
      >

        <div
          className="card"
          style={{
            margin: 0,
            padding: "20px",
            maxWidth: "none",
          }}
        >

          <div style={{ fontSize: "28px" }}>
            🛡️
          </div>

          <strong>Secure</strong>

          <p
            style={{
              fontSize: "13px",
              color: "#667085",
            }}
          >
            Your data is safe
          </p>

        </div>


        <div
          className="card"
          style={{
            margin: 0,
            padding: "20px",
            maxWidth: "none",
          }}
        >

          <div style={{ fontSize: "28px" }}>
            ⚡
          </div>

          <strong>Fast</strong>

          <p
            style={{
              fontSize: "13px",
              color: "#667085",
            }}
          >
            Quick responses
          </p>

        </div>


        <div
          className="card"
          style={{
            margin: 0,
            padding: "20px",
            maxWidth: "none",
          }}
        >

          <div style={{ fontSize: "28px" }}>
            🎯
          </div>

          <strong>Accurate</strong>

          <p
            style={{
              fontSize: "13px",
              color: "#667085",
            }}
          >
            Relevant answers
          </p>

        </div>


        <div
          className="card"
          style={{
            margin: 0,
            padding: "20px",
            maxWidth: "none",
          }}
        >

          <div style={{ fontSize: "28px" }}>
            🗄️
          </div>

          <strong>Powered by RAG</strong>

          <p
            style={{
              fontSize: "13px",
              color: "#667085",
            }}
          >
            Retrieval Augmented Generation
          </p>

        </div>

      </section>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer
        style={{
          marginTop: "50px",
          marginLeft: "-40px",
          marginRight: "-40px",
          marginBottom: "-50px",
          padding: "28px 20px",
          background: "#06162b",
          borderTop: "3px solid #ff7900",
          color: "#ffffff",
          textAlign: "center",
        }}
      >

        © 2026{" "}
        <span
          style={{
            color: "#ff7900",
            fontWeight: "800",
          }}
        >
          VPro Skills
        </span>{" "}
        • All rights reserved.

      </footer>

    </div>
  );
}

export default App;
