export default function EmptyState({ icon: Icon, title, children, action }) {
  return (
    <div className="flex flex-col items-center rounded-lg border border-dashed border-line px-6 py-10 text-center">
      {Icon && <Icon className="mb-3 size-6 text-navy-300" aria-hidden="true" />}
      <p className="font-semibold text-ink">{title}</p>
      {children && <p className="mt-1 max-w-sm text-sm text-ink-3">{children}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
