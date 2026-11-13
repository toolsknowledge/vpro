const STATUS_LABELS = {
  checking: 'Connecting…',
  online: 'Backend connected',
  offline: 'Backend offline',
}

export default function Header({ backendStatus }) {
  return (
    <header className="app-header">
      <div className="brand">
        <img src="/logo.jpeg" alt="VPro Skills EduTech" className="brand-logo" />
        <span className="brand-divider" aria-hidden="true" />
        <div className="brand-text">
          <h1>Corrective RAG Assistant</h1>
          <p>AI-Powered Learning Assistant</p>
        </div>
      </div>
      <span
        className={`status-pill status-${backendStatus}`}
        role="status"
        title={STATUS_LABELS[backendStatus]}
      >
        <span className="status-dot" aria-hidden="true" />
        <span className="status-text">{STATUS_LABELS[backendStatus]}</span>
      </span>
    </header>
  )
}
