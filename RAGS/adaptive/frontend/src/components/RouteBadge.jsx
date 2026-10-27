import { BookOpenText, CircleHelp, Zap } from 'lucide-react';

export const ROUTES = {
  DIRECT: { label: 'DIRECT', description: 'Answered without document retrieval.', icon: Zap },
  RETRIEVE: { label: 'RETRIEVE', description: 'Answered using relevant indexed documents.', icon: BookOpenText },
  CLARIFY: { label: 'CLARIFY', description: 'Asked for more information.', icon: CircleHelp },
};

export default function RouteBadge({ route, grounded = true, compact = false }) {
  const info = ROUTES[route];
  if (!info) return null;
  const Icon = info.icon;
  // A RETRIEVE answer with no relevant context did search, but did not use documents to answer.
  const description =
    route === 'RETRIEVE' && !grounded ? 'Searched the documents; nothing relevant enough was found.' : info.description;
  return (
    <span className={`route-badge route-badge--${route.toLowerCase()}`}>
      <span className="route-badge__label">
        <Icon size={14} aria-hidden="true" /> {info.label}
      </span>
      {!compact && <span className="route-badge__description">{description}</span>}
    </span>
  );
}
