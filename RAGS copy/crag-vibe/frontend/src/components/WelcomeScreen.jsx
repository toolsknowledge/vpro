import { DocumentIcon, RefreshIcon, SparkIcon } from './Icons'

const SAMPLE_QUESTIONS = [
  'What is Python?',
  'Explain Python data types.',
  'What is the difference between List and Tuple?',
  'Explain Python functions.',
  'What is OOPS in Python?',
]

function KnowledgeBaseStatus({ knowledgeBase, isIndexing, onIngest }) {
  if (!knowledgeBase) return null
  if (knowledgeBase.documents.length === 0) {
    return <p className="kb-status kb-warning">No PDF documents were found in the knowledge base.</p>
  }
  return (
    <ul className="kb-list">
      {knowledgeBase.documents.map((doc) => (
        <li key={doc.document_name} className="kb-status">
          <DocumentIcon />
          <span className="kb-name">{doc.document_name}</span>
          <span className="kb-meta">
            {doc.page_count} pages · {doc.indexed ? `${doc.indexed_chunks} chunks indexed` : 'not indexed'}
          </span>
          {!doc.indexed && (
            <button type="button" className="btn btn-small" onClick={onIngest} disabled={isIndexing}>
              <RefreshIcon /> {isIndexing ? 'Indexing…' : 'Index now'}
            </button>
          )}
        </li>
      ))}
    </ul>
  )
}

export default function WelcomeScreen({ onAsk, disabled, knowledgeBase, isIndexing, onIngest }) {
  return (
    <div className="welcome">
      <span className="welcome-badge"><SparkIcon width={14} height={14} /> Learn Smarter with AI-Powered Knowledge Retrieval</span>
      <h2>Welcome to VPro Skills AI Learning Assistant</h2>
      <p className="welcome-subtitle">
        Ask questions about your Python learning materials. I will find relevant information and explain it in
        simple words.
      </p>
      <KnowledgeBaseStatus knowledgeBase={knowledgeBase} isIndexing={isIndexing} onIngest={onIngest} />
      <div className="sample-grid">
        {SAMPLE_QUESTIONS.map((question, index) => (
          <button
            key={question}
            type="button"
            className="sample-card"
            onClick={() => onAsk(question)}
            disabled={disabled}
          >
            <span className="sample-number">{String(index + 1).padStart(2, '0')}</span>
            <span className="sample-text">{question}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
