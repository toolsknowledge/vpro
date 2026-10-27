import { CircleCheck, CircleX, FileSpreadsheet, FileText, FileType, RefreshCw } from 'lucide-react';
import { formatBytes } from '../utils/formatters';

const FILE_ICONS = { xlsx: FileSpreadsheet, pdf: FileType, docx: FileType };

export default function DocumentsPanel({ documents, onRefresh, connection }) {
  return (
    <div className="panel">
      <header className="panel__header panel__header--row">
        <div>
          <h2>Indexed Documents</h2>
          <p>
            Files in <code>{documents?.documents_directory ?? 'backend/data/sample_documents'}</code> and their chunks
            in the vector store.
          </p>
        </div>
        <button type="button" className="button button--secondary" onClick={onRefresh}>
          <RefreshCw size={16} aria-hidden="true" /> Refresh
        </button>
      </header>

      {connection !== 'online' && <p className="notice notice--danger">Backend offline — document list unavailable.</p>}
      {documents && (
        <>
          <p className="muted">
            {documents.indexed_files} of {documents.total_files} file(s) indexed · {documents.total_chunks} chunk(s)
            {!documents.vector_store_ready && ' · vector store unavailable'}
          </p>
          {documents.documents.length === 0 ? (
            <p className="empty-state">No documents found. Run the sample generator script.</p>
          ) : (
            <ul className="document-list">
              {documents.documents.map((doc) => {
                const Icon = FILE_ICONS[doc.file_type] || FileText;
                return (
                  <li key={doc.filename} className="document-row">
                    <Icon size={20} aria-hidden="true" className="document-row__icon" />
                    <div className="document-row__main">
                      <span className="document-row__name">{doc.filename}</span>
                      <span className="document-row__meta">
                        {doc.file_type.toUpperCase() || 'FILE'} · {formatBytes(doc.size_bytes)}
                        {!doc.on_disk && ' · file deleted (run Reindex to remove)'}
                        {!doc.supported && ' · unsupported type'}
                      </span>
                    </div>
                    <span className={`document-row__status${doc.indexed ? ' is-indexed' : ''}`}>
                      {doc.indexed ? <CircleCheck size={16} aria-hidden="true" /> : <CircleX size={16} aria-hidden="true" />}
                      {doc.indexed ? `${doc.chunk_count} chunks` : 'Not indexed'}
                    </span>
                  </li>
                );
              })}
            </ul>
          )}
        </>
      )}
    </div>
  );
}
