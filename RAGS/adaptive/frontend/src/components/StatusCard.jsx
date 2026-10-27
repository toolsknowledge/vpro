export default function StatusCard({ icon: Icon, label, value, detail, tone = 'neutral' }) {
  return (
    <div className={`status-card status-card--${tone}`}>
      {Icon && (
        <span className="status-card__icon" aria-hidden="true">
          <Icon size={18} />
        </span>
      )}
      <div className="status-card__body">
        <span className="status-card__label">{label}</span>
        <span className="status-card__value">{value}</span>
        {detail && <span className="status-card__detail">{detail}</span>}
      </div>
    </div>
  );
}
