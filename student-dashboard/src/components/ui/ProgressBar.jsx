export default function ProgressBar({ value, label, tone = 'brand', size = 'md', className = '' }) {
  const fill = { brand: 'bg-brand', navy: 'bg-navy-700', ok: 'bg-ok' }[tone]
  const height = size === 'sm' ? 'h-1.5' : 'h-2'
  return (
    <div
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={label}
      className={`${height} w-full overflow-hidden rounded-full bg-navy-100 ${className}`}
    >
      <div className={`h-full rounded-full ${fill} transition-[width] duration-500`} style={{ width: `${value}%` }} />
    </div>
  )
}
