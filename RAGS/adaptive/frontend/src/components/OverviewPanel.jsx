import { Database, Gauge, KeyRound, Layers, Sparkles, Wifi } from 'lucide-react';
import RouteBadge, { ROUTES } from './RouteBadge';
import StatusCard from './StatusCard';
import { formatScore } from '../utils/formatters';

const ROUTE_DETAILS = {
  DIRECT: 'Greetings and general questions. The LLM answers immediately; ChromaDB is not queried and no sources are shown.',
  RETRIEVE:
    'Questions about the course documents. The question is embedded, the closest chunks are fetched from ChromaDB, and only chunks above the relevance threshold are given to the LLM, which must answer from them and cite them.',
  CLARIFY:
    'Ambiguous questions such as “Explain it.” with no earlier topic. The assistant asks a short follow-up instead of guessing; no retrieval runs.',
};

export default function OverviewPanel({ connection, health, indexing }) {
  const online = connection === 'online';
  return (
    <div className="panel">
      <header className="panel__header">
        <h2>Overview</h2>
        <p>How this assistant decides what to do with each question, and the current system state.</p>
      </header>

      <div className="status-grid">
        <StatusCard
          icon={Wifi}
          label="Backend"
          value={online ? 'Connected' : connection === 'checking' ? 'Checking…' : 'Offline'}
          tone={online ? 'success' : connection === 'checking' ? 'neutral' : 'danger'}
        />
        <StatusCard
          icon={KeyRound}
          label="OpenAI"
          value={!health ? '—' : health.openai_configured ? 'Configured' : 'API key missing'}
          detail={health && !health.openai_configured ? 'Set OPENAI_API_KEY in backend/.env' : undefined}
          tone={!health ? 'neutral' : health.openai_configured ? 'success' : 'warning'}
        />
        <StatusCard
          icon={Database}
          label="Indexed chunks"
          value={indexing ? indexing.chunk_count : '—'}
          detail={indexing ? `${indexing.document_count} document(s) in “${indexing.collection_name}”` : undefined}
          tone={indexing?.chunk_count ? 'success' : 'warning'}
        />
        <StatusCard icon={Sparkles} label="Chat model" value={health?.chat_model ?? '—'} />
        <StatusCard icon={Layers} label="Embedding model" value={health?.embedding_model ?? '—'} />
        <StatusCard
          icon={Gauge}
          label="Retrieval"
          value={health ? `Top ${health.top_k}` : '—'}
          detail={health ? `Relevance threshold ${formatScore(health.relevance_threshold)}` : undefined}
        />
      </div>

      <h3 className="panel__subheading">The three routes</h3>
      <div className="route-explainer">
        {Object.keys(ROUTES).map((route) => (
          <div key={route} className="route-explainer__item">
            <RouteBadge route={route} />
            <p>{ROUTE_DETAILS[route]}</p>
          </div>
        ))}
      </div>
      <p className="muted">
        Routing is decided per question by an LLM classifier that also sees the last few messages of your chat, so a
        follow-up like “What about the second one?” can be resolved from context. If the classifier returns invalid
        output, the question falls back to RETRIEVE, where the relevance check prevents ungrounded answers.
      </p>
    </div>
  );
}
