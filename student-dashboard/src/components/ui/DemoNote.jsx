import { Info } from 'lucide-react'

// Marks behaviour that is simulated in this prototype rather than a real integration.
export default function DemoNote({ children, className = '' }) {
  return (
    <p className={`flex items-start gap-2 rounded-lg bg-navy-50 px-3 py-2 text-[13px] text-ink-2 ${className}`}>
      <Info className="mt-0.5 size-4 shrink-0 text-navy-500" aria-hidden="true" />
      <span>{children}</span>
    </p>
  )
}
