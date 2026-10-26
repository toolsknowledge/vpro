// A clickable summary tile that leads to the full view for its number.
// The indicator (children) always sits on the bottom edge so all four tiles line up.
export default function StatCard({ icon: Icon, label, value, detail, children, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="group flex min-w-0 flex-col rounded-card border border-line bg-white p-4 text-left transition-colors hover:border-navy-300 sm:p-5"
    >
      <span className="flex items-center justify-between gap-3">
        <span className="text-sm font-medium text-ink-2">{label}</span>
        <span className="hidden size-9 shrink-0 items-center justify-center rounded-lg bg-navy-50 text-navy-700 transition-colors group-hover:bg-navy-900 group-hover:text-brand sm:inline-flex">
          <Icon className="size-[18px]" aria-hidden="true" />
        </span>
      </span>
      <span className="tabular mt-2 font-display text-[28px] leading-none font-bold text-ink sm:text-[30px]">{value}</span>
      <span className="mt-1.5 text-[13px] text-ink-3">{detail}</span>
      {children && <span className="mt-auto block pt-4">{children}</span>}
    </button>
  )
}
