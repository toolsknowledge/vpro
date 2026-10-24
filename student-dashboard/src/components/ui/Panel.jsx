// A titled content block. Panels are the main surface of every view.
export default function Panel({ title, description, action, children, className = '', bodyClassName = '', id }) {
  const headingId = id ? `${id}-title` : undefined
  return (
    <section id={id} aria-labelledby={headingId} className={`@container min-w-0 rounded-card border border-line bg-white ${className}`}>
      {(title || action) && (
        <header className="flex flex-wrap items-start justify-between gap-x-4 gap-y-2 px-5 pt-5 pb-4">
          <div className="min-w-0">
            <h2 id={headingId} className="text-[17px] font-semibold">
              {title}
            </h2>
            {description && <p className="mt-0.5 text-[13px] text-ink-3">{description}</p>}
          </div>
          {action}
        </header>
      )}
      <div className={`px-5 pb-5 ${bodyClassName}`}>{children}</div>
    </section>
  )
}
