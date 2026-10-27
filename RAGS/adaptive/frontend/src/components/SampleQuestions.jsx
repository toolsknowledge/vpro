import RouteBadge from './RouteBadge';

const GROUPS = [
  { key: 'DIRECT', title: 'Designed to route DIRECT', route: 'DIRECT' },
  { key: 'RETRIEVE', title: 'Designed to route RETRIEVE', route: 'RETRIEVE' },
  { key: 'CLARIFY', title: 'Designed to route CLARIFY (in a new chat)', route: 'CLARIFY' },
  { key: 'BORDERLINE', title: 'Borderline — DIRECT or RETRIEVE are both reasonable' },
  { key: 'OUT_OF_SCOPE', title: 'Out of scope — expect “not found in the documents”' },
];

export default function SampleQuestions({ sampleQuestions, onSelect, compact = false }) {
  if (!sampleQuestions) {
    return <p className="muted">Sample questions load from the backend once it is connected.</p>;
  }

  const groups = compact ? GROUPS.slice(0, 3) : GROUPS;
  return (
    <div className={`sample-questions${compact ? ' sample-questions--compact' : ''}`}>
      {!compact && sampleQuestions.note && <p className="sample-questions__note">{sampleQuestions.note}</p>}
      {groups.map(({ key, title, route }) => {
        const questions = sampleQuestions[key] || [];
        if (questions.length === 0) return null;
        return (
          <section key={key} className="sample-group">
            <h3 className="sample-group__title">
              {route && <RouteBadge route={route} compact />}
              <span>{title}</span>
            </h3>
            <ul className="sample-group__list">
              {(compact ? questions.slice(0, 2) : questions).map((question) => (
                <li key={question}>
                  <button type="button" className="sample-chip" onClick={() => onSelect(question)}>
                    {question}
                  </button>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
      {compact && <p className="sample-questions__note">Expected routes only — the actual route is shown on each answer.</p>}
    </div>
  );
}
