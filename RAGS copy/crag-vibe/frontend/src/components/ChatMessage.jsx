import { useState } from 'react'
import FormattedText from './FormattedText'
import { AlertIcon, ChevronIcon, DocumentIcon, FlowIcon, RefreshIcon } from './Icons'
import { RELEVANCE_LABELS, RETRIEVAL_STATUS_INFO } from '../workflow'

function SourcesList({ sources }) {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <div className="sources">
      <button
        type="button"
        className="sources-toggle"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((open) => !open)}
      >
        <DocumentIcon width={16} height={16} />
        Sources ({sources.length})
        <ChevronIcon width={16} height={16} className={`chevron ${isOpen ? 'chevron-open' : ''}`} />
      </button>
      {isOpen && (
        <ul className="source-list">
          {sources.map((source) => (
            <li key={source.chunk_id} className="source-card">
              <div className="source-header">
                <span className="source-name">{source.document_name}</span>
                <span className="source-page">Page {source.page_number}</span>
                <span className={`relevance relevance-${source.relevance}`}>
                  {RELEVANCE_LABELS[source.relevance]}
                </span>
              </div>
              <p className="source-snippet">{source.snippet}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export function AssistantMessage({ response, isSelected, onSelect }) {
  const statusInfo = RETRIEVAL_STATUS_INFO[response.retrieval_status]
  return (
    <div className={`message message-assistant ${isSelected ? 'is-selected' : ''}`}>
      <div className="avatar" aria-hidden="true">AI</div>
      <div className="bubble">
        <FormattedText text={response.answer} />
        <div className="message-meta">
          <span className={`badge badge-${statusInfo.tone}`}>{statusInfo.label}</span>
          <span className="meta-text">
            {response.corrective_retrieval_used
              ? `Corrective retrieval: ${response.correction_attempts} attempt${response.correction_attempts === 1 ? '' : 's'}`
              : 'No correction needed'}
          </span>
          <button type="button" className="link-button" onClick={onSelect}>
            <FlowIcon width={15} height={15} /> View workflow
          </button>
        </div>
        {response.sources.length > 0 && <SourcesList sources={response.sources} />}
      </div>
    </div>
  )
}

export function UserMessage({ text }) {
  return (
    <div className="message message-user">
      <div className="bubble">{text}</div>
    </div>
  )
}

export function ErrorMessage({ text, onRetry, disabled }) {
  return (
    <div className="message message-assistant" role="alert">
      <div className="avatar avatar-error" aria-hidden="true"><AlertIcon width={16} height={16} /></div>
      <div className="bubble bubble-error">
        <p>{text}</p>
        {onRetry && (
          <button type="button" className="btn btn-small btn-outline" onClick={onRetry} disabled={disabled}>
            <RefreshIcon width={15} height={15} /> Try again
          </button>
        )}
      </div>
    </div>
  )
}

export function TypingIndicator() {
  return (
    <div className="message message-assistant" aria-label="Assistant is thinking">
      <div className="avatar" aria-hidden="true">AI</div>
      <div className="bubble bubble-typing">
        <span className="typing-dots" aria-hidden="true"><span /><span /><span /></span>
        <span className="typing-text">Searching the learning materials and checking relevance…</span>
      </div>
    </div>
  )
}
