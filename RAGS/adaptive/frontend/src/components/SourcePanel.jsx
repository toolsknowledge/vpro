import { ChevronDown, FileText, SearchX } from 'lucide-react';
import { chunkLocation, formatScore, pluralize } from '../utils/formatters';

export default function SourcePanel({ response }) {
  if (!response.retrieval_performed) {
    return <p className="source-note">No documents were searched for this answer.</p>;
  }

  if (response.sources.length === 0) {
    return (
      <div className="source-empty">
        <SearchX size={18} aria-hidden="true" />
        <span>
          {response.retrieval_count === 0
            ? 'No indexed chunks were available to search.'
            : `Searched ${pluralize(response.retrieval_count, 'chunk')}; the best relevance was ${formatScore(
                response.relevance_score,
              )}, below the ${formatScore(response.relevance_threshold)} threshold. No sources were used.`}
        </span>
      </div>
    );
  }

  return (
    <section className="source-panel" aria-label="Sources used for this answer">
      <h4 className="source-panel__title">
        Sources · {pluralize(response.sources.length, 'chunk')} above the {formatScore(response.relevance_threshold)}{' '}
        relevance threshold
      </h4>
      <ol className="source-list">
        {response.sources.map((source, index) => (
          <li key={source.chunk_id}>
            <details className="source-card">
              <summary>
                <span className="source-card__number">[{index + 1}]</span>
                <FileText size={16} aria-hidden="true" className="source-card__icon" />
                <span className="source-card__name">{source.source}</span>
                <span className="source-card__score" title="Cosine similarity between your question and this chunk">
                  {formatScore(source.relevance)}
                </span>
                <ChevronDown size={16} aria-hidden="true" className="source-card__chevron" />
              </summary>
              <div className="source-card__body">
                {chunkLocation(source) && <p className="source-card__meta">{chunkLocation(source)}</p>}
                <blockquote>{source.snippet}</blockquote>
              </div>
            </details>
          </li>
        ))}
      </ol>
    </section>
  );
}
