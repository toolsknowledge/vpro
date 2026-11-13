import { useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const fileInput = useRef(null);

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [uploadInfo, setUploadInfo] = useState(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");
  const [showChunks, setShowChunks] = useState(false);

  async function uploadPDF() {
    if (!file) {
      setError("Please select a PDF file first.");
      return;
    }

    setUploading(true);
    setError("");
    setUploaded(false);
    setUploadInfo(null);
    setMessages([]);
    setShowChunks(false);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/upload-pdf`, {     /** http://127.0.0.1:8000/upload-pdf */
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "PDF upload failed.");
      }

      setUploaded(true);
      setUploadInfo(data);
    } catch (err) {
      setError(
        err.message || "Cannot connect to the backend. Is FastAPI running?"
      );
    } finally {
      setUploading(false);
    }
  }

  async function askQuestion(text = question) {
    const userQuestion = text.trim();

    if (!userQuestion || asking) return;

    if (!uploaded) {
      setError("Upload and process a PDF before asking questions.");
      return;
    }

    setError("");
    setQuestion("");
    setAsking(true);
    setShowChunks(false);

    setMessages((previous) => [
      ...previous,
      { role: "user", content: userQuestion },
    ]);

    try {
      const response = await fetch(`${API_URL}/ask`, {    /** http://127.0.0.1:8000/ask */
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userQuestion }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to answer the question.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer || "No answer was returned.",
          chunks: data.retrieved_chunks || [],
        },
      ]);
    } catch (err) {
      setError(
        err.message || "Cannot connect to the backend. Is FastAPI running?"
      );
    } finally {
      setAsking(false);
    }
  }

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0];

    setError("");

    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a PDF file.");
      event.target.value = "";
      return;
    }

    setFile(selectedFile);
    setUploaded(false);
    setUploadInfo(null);
    setMessages([]);
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  }

  function startNewDocument() {
    setFile(null);
    setUploaded(false);
    setUploadInfo(null);
    setMessages([]);
    setQuestion("");
    setError("");
    setShowChunks(false);

    if (fileInput.current) {
      fileInput.current.value = "";
    }
  }

  return (
    <div className="rag-app">
      <header className="topbar">
        <div className="brand">
          <img
            src="/src/assets/logo.png"
            alt="VPro Skills"
            className="brand-logo"
          />

          <div className="brand-divider" />

          <div>
            <h1>Naive RAG</h1>
            <p>Document Intelligence</p>
          </div>
        </div>

        <div className="header-status">
          <span className="status-dot" />
          <span>AI Workspace</span>
        </div>
      </header>

      <main className="workspace">
        <section className="welcome-section">
          <div className="eyebrow">
            <span className="eyebrow-dot" />
            RETRIEVAL-AUGMENTED GENERATION
          </div>

          <h2>
            Your documents.
            <br />
            <span>Intelligent answers.</span>
          </h2>

          <p className="welcome-description">
            Upload a PDF, ask questions, and discover answers grounded in
            your document using AI-powered retrieval.
          </p>
        </section>

        <div className="dashboard">
          <aside className="sidebar">
            <div className="panel-heading">
              <div>
                <span className="section-label">YOUR WORKSPACE</span>
                <h3>Knowledge source</h3>
              </div>

              <span className="heading-icon">PDF</span>
            </div>

            <input
              ref={fileInput}
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              hidden
            />

            <button
              type="button"
              className="upload-zone"
              onClick={() => fileInput.current?.click()}
              disabled={uploading}
            >
              <span className="upload-icon">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.7"
                  width="29"
                  height="29"
                >
                  <path d="M12 16V4m-5 5 5-5 5 5" />
                  <path d="M5 14v5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-5" />
                </svg>
              </span>

              <strong>
                {file ? "Choose another PDF" : "Upload your document"}
              </strong>

              <span>Click to browse files</span>
              <span className="file-format">PDF DOCUMENT</span>
            </button>

            {file && (
              <div className="selected-file">
                <div className="pdf-icon">PDF</div>

                <div className="file-details">
                  <strong title={file.name}>{file.name}</strong>
                  <span>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                </div>

                <button
                  type="button"
                  className="remove-file"
                  aria-label="Remove selected file"
                  onClick={() => {
                    setFile(null);
                    setUploaded(false);
                    setUploadInfo(null);
                    if (fileInput.current) fileInput.current.value = "";
                  }}
                >
                  ×
                </button>
              </div>
            )}

            <button
              type="button"
              className="primary-button upload-button"
              onClick={uploadPDF}
              disabled={!file || uploading}
            >
              {uploading ? (
                <>
                  <span className="spinner" />
                  Processing document...
                </>
              ) : uploaded ? (
                "Document processed ✓"
              ) : (
                "Upload & Process PDF →"
              )}
            </button>

            {uploadInfo && (
              <div className="document-stats">
                <div className="success-message">
                  <span>✓</span> Document indexed successfully
                </div>

                <div className="stat-row">
                  <span>Pages processed</span>
                  <strong>{uploadInfo.total_pages}</strong>
                </div>

                <div className="stat-row">
                  <span>Text chunks</span>
                  <strong>{uploadInfo.total_chunks}</strong>
                </div>

                <div className="stat-row">
                  <span>Search engine</span>
                  <strong>FAISS</strong>
                </div>
              </div>
            )}

            <div className="pipeline">
              <span className="section-label">HOW IT WORKS</span>

              {[
                ["01", "Read PDF", "Extract document text"],
                ["02", "Create chunks", "Split into small pieces"],
                ["03", "Find context", "Search relevant information"],
                ["04", "Generate answer", "Use OpenAI to respond"],
              ].map(([number, title, description]) => (
                <div className="pipeline-step" key={number}>
                  <span className="step-number">{number}</span>
                  <div>
                    <strong>{title}</strong>
                    <p>{description}</p>
                  </div>
                </div>
              ))}
            </div>

            <button
              type="button"
              className="secondary-button"
              onClick={startNewDocument}
            >
              + New document
            </button>
          </aside>

          <section className="chat-panel">
            <div className="chat-header">
              <div className="chat-title">
                <div className="ai-avatar">✳</div>
                <div>
                  <h3>Document Assistant</h3>
                  <p>
                    <span className="status-dot" />
                    {uploaded ? "Document ready for questions" : "Ready to help"}
                  </p>
                </div>
              </div>

              <span className="model-tag">OPENAI · RAG</span>
            </div>

            <div className="chat-body">
              {messages.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">
                    <svg
                      viewBox="0 0 48 48"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      width="46"
                      height="46"
                    >
                      <path d="M13 5h16l9 9v28H13z" />
                      <path d="M29 5v10h9M19 24h13M19 30h13M19 36h8" />
                      <path d="M7 12v29h24" />
                    </svg>
                  </div>

                  <h3>
                    {uploaded
                      ? "Your document is ready"
                      : "Start a conversation"}
                  </h3>

                  <p>
                    {uploaded
                      ? "Ask a question about your uploaded PDF. Answers are generated using retrieved document context."
                      : "Upload and process a PDF to start asking questions about its contents."}
                  </p>

                  {uploaded && (
                    <div className="suggestion-list">
                      <span className="suggestion-label">
                        TRY ASKING
                      </span>

                      {[
                        "Summarize this document",
                        "What are the main topics?",
                        "Explain the key points",
                      ].map((item) => (
                        <button
                          type="button"
                          className="suggestion"
                          key={item}
                          onClick={() => askQuestion(item)}
                          disabled={asking}
                        >
                          {item}
                          <span>↗</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div className="messages">
                  {messages.map((message, index) => (
                    <div
                      className={`message-row ${message.role}`}
                      key={`${index}-${message.role}`}
                    >
                      <div className="message-avatar">
                        {message.role === "user" ? "Y" : "✳"}
                      </div>

                      <div className="message-content">
                        <span className="message-author">
                          {message.role === "user" ? "You" : "Document Assistant"}
                        </span>

                        <div className="message-bubble">
                          {message.content}
                        </div>

                        {message.role === "assistant" &&
                          message.chunks?.length > 0 && (
                            <div className="sources">
                              <button
                                type="button"
                                className="source-toggle"
                                onClick={() =>
                                  setShowChunks((current) =>
                                    current === index ? false : index
                                  )
                                }
                              >
                                ▤ {message.chunks.length} retrieved text
                                chunks
                                <span>
                                  {showChunks === index ? "−" : "+"}
                                </span>
                              </button>

                              {showChunks === index && (
                                <div className="source-list">
                                  {message.chunks.map((chunk, chunkIndex) => (
                                    <div
                                      className="source-item"
                                      key={chunkIndex}
                                    >
                                      <strong>
                                        Chunk {chunkIndex + 1}
                                      </strong>
                                      <p>{chunk}</p>
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          )}
                      </div>
                    </div>
                  ))}

                  {asking && (
                    <div className="message-row assistant">
                      <div className="message-avatar">✳</div>
                      <div className="message-content">
                        <span className="message-author">
                          Document Assistant
                        </span>
                        <div className="message-bubble typing">
                          <span />
                          <span />
                          <span />
                          <small>Finding relevant information...</small>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {error && (
              <div className="error-message" role="alert">
                <span>!</span>
                <p>{error}</p>
                <button
                  type="button"
                  onClick={() => setError("")}
                  aria-label="Dismiss error"
                >
                  ×
                </button>
              </div>
            )}

            <div className="composer-area">
              {!uploaded && (
                <p className="upload-hint">
                  Upload and process a PDF to enable document chat.
                </p>
              )}

              <form
                className="composer"
                onSubmit={(event) => {
                  event.preventDefault();
                  askQuestion();
                }}
              >
                <textarea
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={
                    uploaded
                      ? "Ask anything about your document..."
                      : "Upload a PDF to start asking questions..."
                  }
                  rows={2}
                  disabled={!uploaded || asking}
                />

                <button
                  type="submit"
                  className="send-button"
                  disabled={!uploaded || !question.trim() || asking}
                  aria-label="Send question"
                >
                  {asking ? (
                    <span className="spinner" />
                  ) : (
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      width="20"
                      height="20"
                    >
                      <path d="M22 2 11 13" />
                      <path d="m22 2-7 20-4-9-9-4z" />
                    </svg>
                  )}
                </button>
              </form>

              <div className="composer-footer">
                <span>↵ Enter to send · Shift + Enter for new line</span>
                <span>Powered by OpenAI</span>
              </div>
            </div>
          </section>
        </div>

        <footer className="page-footer">
          <span>VPro Skills · Document Intelligence</span>
          <span>Built with FastAPI, FAISS & OpenAI</span>
        </footer>
      </main>
    </div>
  );
}