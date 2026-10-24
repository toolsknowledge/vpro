import { Braces, Cloud, Coffee, Database, GitBranch, Layers, Sparkles } from 'lucide-react'

// Course visuals are drawn, not photographed: a navy tile with a pattern that hints at the subject.
const themes = {
  python: { icon: Braces, bg: '#13254d' },
  java: { icon: Coffee, bg: '#1c3366' },
  mern: { icon: Layers, bg: '#203a6e' },
  ai: { icon: Sparkles, bg: '#0c1834' },
  sql: { icon: Database, bg: '#284583' },
  git: { icon: GitBranch, bg: '#1c3366' },
  cloud: { icon: Cloud, bg: '#3a5594' },
}

export default function CourseThumb({ pattern, className = '', compact = false }) {
  const { icon: Icon, bg } = themes[pattern] ?? themes.python
  if (compact) {
    return (
      <span aria-hidden="true" className={`inline-flex shrink-0 items-center justify-center rounded-lg ${className}`} style={{ backgroundColor: bg }}>
        <Icon className="size-5 text-brand" />
      </span>
    )
  }
  return (
    <div aria-hidden="true" className={`relative overflow-hidden ${className}`} style={{ backgroundColor: bg }}>
      <svg className="absolute inset-0 size-full opacity-[0.14]" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id={`grid-${pattern}`} width="18" height="18" patternUnits="userSpaceOnUse">
            <path d="M18 0H0V18" fill="none" stroke="white" strokeWidth="1" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill={`url(#grid-${pattern})`} />
      </svg>
      <span className="absolute top-3 left-3 inline-flex size-9 items-center justify-center rounded-lg bg-white/10 ring-1 ring-white/20">
        <Icon className="size-5 text-brand" />
      </span>
    </div>
  )
}
