import { Database, KeyRound, LoaderCircle, Menu, Wifi, WifiOff } from 'lucide-react';
import { pluralize } from '../utils/formatters';

function ConnectionPill({ connection }) {
  if (connection === 'checking') {
    return (
      <span className="pill pill--neutral">
        <LoaderCircle size={14} className="spin" aria-hidden="true" /> Checking backend
      </span>
    );
  }
  return connection === 'online' ? (
    <span className="pill pill--success">
      <Wifi size={14} aria-hidden="true" /> Backend connected
    </span>
  ) : (
    <span className="pill pill--danger">
      <WifiOff size={14} aria-hidden="true" /> Backend offline
    </span>
  );
}

function IndexPill({ indexing }) {
  if (!indexing) return null;
  if (indexing.is_indexing) {
    return (
      <span className="pill pill--neutral">
        <LoaderCircle size={14} className="spin" aria-hidden="true" /> Indexing…
      </span>
    );
  }
  return indexing.chunk_count > 0 ? (
    <span className="pill pill--success">
      <Database size={14} aria-hidden="true" /> {pluralize(indexing.document_count, 'doc')} ·{' '}
      {pluralize(indexing.chunk_count, 'chunk')}
    </span>
  ) : (
    <span className="pill pill--warning">
      <Database size={14} aria-hidden="true" /> Not indexed
    </span>
  );
}

export default function Header({ connection, health, indexing, onToggleMenu, menuOpen }) {
  return (
    <header className="app-header">
      <button
        type="button"
        className="icon-button menu-toggle"
        onClick={onToggleMenu}
        aria-label={menuOpen ? 'Close navigation' : 'Open navigation'}
        aria-expanded={menuOpen}
        aria-controls="app-sidebar"
      >
        <Menu size={22} />
      </button>
      <img src="/logo.png" alt="VPRO Skills logo" className="brand-logo" width="271" height="186" />
      <div className="brand-text">
        <h1>Adaptive RAG Assistant</h1>
        <p>Intelligent document question answering</p>
      </div>
      <div className="header-status" aria-live="polite">
        <ConnectionPill connection={connection} />
        {connection === 'online' && <IndexPill indexing={indexing} />}
        {connection === 'online' && health && !health.openai_configured && (
          <span className="pill pill--warning" title="Set OPENAI_API_KEY in backend/.env and restart the backend">
            <KeyRound size={14} aria-hidden="true" /> API key missing
          </span>
        )}
      </div>
    </header>
  );
}
