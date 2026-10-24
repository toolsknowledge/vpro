const sizes = { sm: 'size-8 text-xs', md: 'size-10 text-sm', lg: 'size-16 text-xl' }

export default function Avatar({ name, size = 'md' }) {
  const initials = name
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
  return (
    <span
      aria-hidden="true"
      className={`inline-flex shrink-0 items-center justify-center rounded-full bg-navy-900 font-display font-bold text-white ring-2 ring-brand ring-offset-2 ring-offset-white ${sizes[size]}`}
    >
      {initials}
    </span>
  )
}
