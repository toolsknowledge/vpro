import { useState } from 'react';
import { CircleCheck, Database, FileText, Layers, LoaderCircle, RefreshCw } from 'lucide-react';
import { api } from '../api/client';
import StatusCard from './StatusCard';
import { formatDateTime, formatDuration, formatStatus } from '../utils/formatters';

const STATUS_TONE = { success: 'success', partial: 'warning', failed: 'danger', no_documents: 'warning' };

function ResultDetails({ result }) {
  return (
    <div className={`notice notice--${STATUS_TONE[result.status] || 'neutral'}`}>
      <p>
        <strong>
          Last {result.mode}: {formatStatus(result.status)}
        </strong>{' '}
        — {result.message}
      </p>
      <p className="notice__meta">
        {formatDateTime(result.finished_at)} · {formatDuration(result.duration_seconds)} · discovered{' '}
        {result.discovered_files} · processed {result.processed_files} · unchanged {result.unchanged_files} · chunks
        created {result.chunks_created} · chunks removed {result.chunks_removed}
      </p>
      {result.removed_sources.length > 0 && <p>Removed from index: {result.removed_sources.join(', ')}</p>}
      {result.skipped_files.length > 0 && (
        <>
          <p>Skipped:</p>
          <ul>
            {result.skipped_files.map((item) => (
              <li key={item.filename}>
                {item.filename} — {item.reason}
              </li>
            ))}
          </ul>
        </>
      )}
      {result.errors.length > 0 && (
        <>
          <p>Errors:</p>
          <ul>
            {result.errors.map((item) => (
              <li key={item.filename}>
                {item.filename} — {item.reason}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default function IndexingPanel({ indexing, health, connection, onIndexed }) {
  const [running, setRunning] = useState(null); // 'index' | 'reindex' | null
  const [error, setError] = useState(null);

  const run = async (mode) => {
    setRunning(mode);
    setError(null);
    try {
      await (mode === 'index' ? api.indexDocuments() : api.reindexDocuments());
    } catch (err) {
      setError(err.message);
    } finally {
      setRunning(null);
      onIndexed();
    }
  };

  const offline = connection !== 'online';
  const busy = running !== null || indexing?.is_indexing;

  return (
    <div className="panel">
      <header className="panel__header">
        <h2>Indexing Controls</h2>
        <p>
          <strong>Index Documents</strong> embeds new or changed files and skips unchanged ones.{' '}
          <strong>Reindex Documents</strong> re-embeds every file and removes chunks of deleted files. Both call the
          OpenAI embeddings API, which may incur charges.
        </p>
      </header>

      <div className="status-grid">
        <StatusCard
          icon={FileText}
          label="Indexed files"
          value={indexing ? indexing.document_count : '—'}
          tone={indexing?.document_count ? 'success' : 'warning'}
        />
        <StatusCard icon={Layers} label="Chunks" value={indexing ? indexing.chunk_count : '—'} />
        <StatusCard
          icon={Database}
          label="Collection"
          value={indexing ? indexing.collection_name : '—'}
          detail={indexing ? (indexing.vector_store_ready ? 'Ready' : indexing.vector_store_error) : undefined}
          tone={indexing ? (indexing.vector_store_ready ? 'success' : 'danger') : 'neutral'}
        />
        <StatusCard
          icon={CircleCheck}
          label="Last run"
          value={indexing?.last_result ? formatStatus(indexing.last_result.status) : 'Never'}
          detail={indexing?.last_result ? formatDateTime(indexing.last_result.finished_at) : undefined}
          tone={indexing?.last_result ? STATUS_TONE[indexing.last_result.status] : 'neutral'}
        />
      </div>

      {health && !health.openai_configured && (
        <p className="notice notice--warning">
          OPENAI_API_KEY is not configured. Add it to <code>backend/.env</code> and restart the backend before indexing.
        </p>
      )}

      <div className="button-row">
        <button type="button" className="button button--primary" onClick={() => run('index')} disabled={busy || offline}>
          {running === 'index' ? <LoaderCircle size={16} className="spin" aria-hidden="true" /> : <Database size={16} aria-hidden="true" />}
          {running === 'index' ? 'Indexing…' : 'Index Documents'}
        </button>
        <button type="button" className="button button--secondary" onClick={() => run('reindex')} disabled={busy || offline}>
          {running === 'reindex' ? <LoaderCircle size={16} className="spin" aria-hidden="true" /> : <RefreshCw size={16} aria-hidden="true" />}
          {running === 'reindex' ? 'Reindexing…' : 'Reindex Documents'}
        </button>
      </div>

      {running && (
        <p className="notice notice--neutral" role="status">
          {running === 'index' ? 'Indexing' : 'Reindexing'} documents — extracting text, chunking and embedding. This
          usually takes a few seconds.
        </p>
      )}
      {error && (
        <p className="notice notice--danger" role="alert">
          {error}
        </p>
      )}
      {indexing?.last_result && !running && <ResultDetails result={indexing.last_result} />}
      {offline && <p className="notice notice--danger">Backend offline — indexing is unavailable.</p>}
    </div>
  );
}
