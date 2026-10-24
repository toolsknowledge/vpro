const base =
  'inline-flex items-center justify-center gap-2 rounded-xl font-semibold whitespace-nowrap transition duration-200 ease-out active:translate-y-px disabled:opacity-50'

const variants = {
  primary: 'bg-brand text-ink shadow-[0_6px_16px_-8px_rgb(242_138_36/0.9)] hover:bg-brand-deep hover:-translate-y-0.5',
  dark: 'bg-ink text-white hover:bg-ink-soft',
  secondary: 'bg-white text-ink ring-1 ring-line hover:ring-ink/30 hover:-translate-y-0.5',
  ghost: 'text-ink hover:bg-ink/5',
}

const sizes = {
  sm: 'h-10 px-4 text-sm',
  md: 'h-11 px-5 text-[15px]',
  lg: 'h-13 px-6 text-base',
}

export default function Button({ as: Tag = 'a', variant = 'primary', size = 'md', className = '', children, ...props }) {
  return (
    <Tag className={`${base} ${variants[variant]} ${sizes[size]} ${className}`} {...props}>
      {children}
    </Tag>
  )
}
