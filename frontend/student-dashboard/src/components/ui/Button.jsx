const variants = {
  primary: 'bg-navy-900 text-white hover:bg-navy-800 active:bg-navy-950',
  accent: 'bg-brand text-navy-950 hover:bg-[#f59a33] active:bg-brand-600',
  soft: 'bg-navy-50 text-navy-900 hover:bg-navy-100 active:bg-navy-100',
  secondary: 'border border-line bg-white text-navy-900 hover:border-navy-300 hover:bg-navy-50',
  ghost: 'text-navy-700 hover:bg-navy-50 hover:text-navy-900',
}

const sizes = {
  sm: 'h-8 px-3 text-[13px] gap-1.5',
  md: 'h-10 px-4 text-sm gap-2',
}

export default function Button({ variant = 'secondary', size = 'md', className = '', icon: Icon, children, ...props }) {
  return (
    <button
      type="button"
      className={`inline-flex shrink-0 items-center justify-center rounded-lg font-semibold whitespace-nowrap transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {Icon && <Icon className="size-4" aria-hidden="true" />}
      {children}
    </button>
  )
}
