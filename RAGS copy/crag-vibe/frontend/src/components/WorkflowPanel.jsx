import { useState } from 'react'
import { ChevronIcon, FlowIcon } from './Icons'
import {
  RELEVANCE_LABELS,
  RETRIEVAL_STATUS_INFO,
  STATUS_LABELS,
  buildIdleStages,
  buildLoadingStages,
  buildWorkflowStages,
} from '../workflow'

function StageList({ stages }) {
  return (
    <ol className="stage-list">
      {stages.map((stage, index) => (
        <li key={stage.name} className={`stage stage-${stage.status}`}>
          <span className="stage-marker" aria-hidden="true">{index + 1}</span>
          <div className="stage-content">
            <div className="stage-header">
              <h4>{stage.name}</h4>
              <span className={`stage-status status-badge-${stage.status}`}>{STATUS_LABELS[stage.status]}</span>
            </div>
            <p className="stage-explanation">{stage.explanation}</p>
            {stage.details.length > 0 && (
              <ul className="stage-details">
                {stage.details.map((detail, index) => <li key={index}>{detail}</li>)}
              </ul>
            )}
          </div>
        </li>
      ))}
    </ol>
  )
}

function AttemptsTable({ attempts }) {
  return (
    <div className="panel-section">
      <h3>Retrieval attempts</h3>
      <div className="attempts">
        {attempts.map((attempt) => (
          <div key={attempt.attempt_number} className={`attempt ${attempt.sufficient ? 'attempt-ok' : 'attempt-bad'}`}>
            <div className="attempt-header">
              <span className="attempt-title">
                {attempt.attempt_number === 0 ? 'Initial retrieval' : `Correction ${attempt.attempt_number}`}
              </span>
              <span className={`badge ${attempt.sufficient ? 'badge-success' : 'badge-danger'}`}>
                {attempt.sufficient ? 'Relevant' : 'Not relevant'}
              </span>
            </div>
            <p className="attempt-query">“{attempt.query}”</p>
            {attempt.rewrite_reason && <p className="attempt-reason">Why rewritten: {attempt.rewrite_reason}</p>}
            <div className="grade-bar" aria-label="Relevance of retrieved chunks">
              <span className="grade grade-relevant" title="Relevant">{attempt.relevant_count} relevant</span>
              <span className="grade grade-partially_relevant" title="Partially relevant">{attempt.partially_relevant_count} partial</span>
              <span className="grade grade-irrelevant" title="Irrelevant">{attempt.irrelevant_count} irrelevant</span>
            </div>
            <p className="attempt-summary">{attempt.evaluation_summary}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function RetrievedDocuments({ documents }) {
  const [expandedId, setExpandedId] = useState(null)
  return (
    <div className="panel-section">
      <h3>Retrieved chunks ({documents.length})</h3>
      <ul className="retrieved-list">
        {documents.map((doc) => {
          const key = `${doc.attempt}-${doc.chunk_id}`
          const isExpanded = expandedId === key
          return (
            <li key={key} className="retrieved-item">
              <button
                type="button"
                className="retrieved-toggle"
                aria-expanded={isExpanded}
                onClick={() => setExpandedId(isExpanded ? null : key)}
              >
                <span className={`relevance relevance-${doc.relevance}`}>{RELEVANCE_LABELS[doc.relevance]}</span>
                <span className="retrieved-page">Page {doc.page_number}</span>
                <span className="retrieved-attempt">{doc.attempt === 0 ? 'Initial' : `Correction ${doc.attempt}`}</span>
                <span className="similarity" title="Similarity score from ChromaDB">
                  <span className="similarity-bar"><span style={{ width: `${Math.round(doc.similarity * 100)}%` }} /></span>
                  {doc.similarity.toFixed(2)}
                </span>
                <ChevronIcon width={14} height={14} className={`chevron ${isExpanded ? 'chevron-open' : ''}`} />
              </button>
              <p className="retrieved-reason">{doc.reason}</p>
              {isExpanded && (
                <pre className="retrieved-text">{doc.text}</pre>
              )}
            </li>
          )
        })}
      </ul>
    </div>
  )
}

export default function WorkflowPanel({ response, isLoading, pendingQuestion }) {
  const [isOpen, setIsOpen] = useState(false)

  let stages = buildIdleStages()
  if (isLoading) stages = buildLoadingStages(pendingQuestion)
  else if (response) stages = buildWorkflowStages(response)
  const statusInfo = !isLoading && response ? RETRIEVAL_STATUS_INFO[response.retrieval_status] : null

  return (
    <aside className={`workflow-panel ${isOpen ? 'is-open' : ''}`} aria-label="How Corrective RAG Works">
      <button
        type="button"
        className="panel-toggle"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((open) => !open)}
      >
        <FlowIcon />
        <span>How Corrective RAG Works</span>
        {statusInfo && <span className={`badge badge-${statusInfo.tone}`}>{statusInfo.label}</span>}
        <ChevronIcon className={`chevron ${isOpen ? 'chevron-open' : ''}`} />
      </button>

      <div className="panel-body">
        {statusInfo ? (
          <div className={`panel-summary summary-${statusInfo.tone}`}>
            <strong>{statusInfo.label}</strong>
            <span>{statusInfo.text}</span>
          </div>
        ) : (
          <p className="panel-intro">
            {isLoading
              ? 'Working on your question…'
              : 'Ask a question to see each step of Corrective RAG for your answer.'}
          </p>
        )}

        <StageList stages={stages} />

        {!isLoading && response && (
          <>
            <AttemptsTable attempts={response.attempts} />
            <RetrievedDocuments documents={response.retrieved_documents} />
          </>
        )}
      </div>
    </aside>
  )
}
