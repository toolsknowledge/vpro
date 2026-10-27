export default function LoadingIndicator({ label = 'Routing your question and preparing an answer…' }) {
  return (
    <div className="loading-indicator" role="status" aria-live="polite">
      <span className="loading-dots" aria-hidden="true">
        <span />
        <span />
        <span />
      </span>
      <span>{label}</span>
    </div>
  );
}
