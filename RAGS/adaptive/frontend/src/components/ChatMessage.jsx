import { useEffect, useRef, useState } from 'react';
import { Bot, Check, Copy, RotateCcw, TriangleAlert } from 'lucide-react';
import RouteBadge from './RouteBadge';
import SourcePanel from './SourcePanel';
import { formatScore, pluralize } from '../utils/formatters';

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  const timerRef = useRef(null);
  useEffect(() => () => clearTimeout(timerRef.current), []);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };

  return (
    <button type="button" className="icon-button icon-button--small" onClick={copy} aria-label="Copy answer">
      {copied ? <Check size={16} /> : <Copy size={16} />}
      <span className="icon-button__text">{copied ? 'Copied' : 'Copy'}</span>
    </button>
  );
}

function RetrievalSummary({ response }) {
  if (!response.retrieval_performed) return null;
  return (
    <span className="message-meta__item">
      Retrieved {pluralize(response.retrieval_count, 'chunk')} · top relevance {formatScore(response.relevance_score)}
    </span>
  );
}

export default function ChatMessage({ message, onRetry, retryDisabled }) {
  if (message.role === 'user') {
    return (
      <div className="message message--user">
        <div className="message__bubble">{message.content}</div>
      </div>
    );
  }

  if (message.role === 'error') {
    return (
      <div className="message message--error" role="alert">
        <TriangleAlert size={18} aria-hidden="true" />
        <div className="message__error-body">
          <p>{message.content}</p>
          {message.retryable && (
            <button
              type="button"
              className="button button--secondary button--small"
              onClick={() => onRetry(message.id)}
              disabled={retryDisabled}
            >
              <RotateCcw size={14} aria-hidden="true" /> Retry
            </button>
          )}
        </div>
      </div>
    );
  }

  const { response } = message;
  return (
    <article className="message message--assistant">
      <span className="message__avatar" aria-hidden="true">
        <Bot size={18} />
      </span>
      <div className="message__content">
        <div className="message__route">
          <RouteBadge route={response.route} grounded={response.grounded} />
          <p className="message__reason">
            <strong>Why this route:</strong> {response.reason}
            {response.classifier_fallback && ' (fallback route)'}
          </p>
        </div>
        <div className="message__answer">{message.content}</div>
        <div className="message-meta">
          <RetrievalSummary response={response} />
          <CopyButton text={message.content} />
        </div>
        <SourcePanel response={response} />
      </div>
    </article>
  );
}
