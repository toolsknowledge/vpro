// Segmented filter control built from toggle buttons (aria-pressed).
export default function FilterTabs({ options, value, onChange, label }) {
  return (
    <div role="group" aria-label={label} className="inline-flex max-w-full flex-wrap gap-1 rounded-lg bg-navy-50 p-1">
      {options.map((opt) => {
        const active = opt.value === value
        return (
          <button
            key={opt.value}
            type="button"
            aria-pressed={active}
            onClick={() => onChange(opt.value)}
            className={`inline-flex h-8 items-center gap-1.5 rounded-md px-3 text-[13px] font-semibold whitespace-nowrap transition-colors ${
              active ? 'bg-white text-navy-900 shadow-sm ring-1 ring-line' : 'text-ink-2 hover:text-navy-900'
            }`}
          >
            {opt.label}
            {opt.count !== undefined && (
              <span className={`tabular rounded px-1.5 text-xs ${active ? 'bg-navy-100 text-navy-900' : 'bg-white/70 text-ink-3'}`}>
                {opt.count}
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
