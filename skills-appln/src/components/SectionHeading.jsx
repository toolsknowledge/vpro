const tones = {
  light: { title: 'text-ink', intro: 'text-slate' },
  dark: { title: 'text-white', intro: 'text-white/70' },
  brand: { title: 'text-ink', intro: 'text-ink/80' },
}

export default function SectionHeading({ title, intro, tone = 'light', className = '' }) {
  const t = tones[tone]
  return (
    <div className={`max-w-2xl ${className}`}>
      <h2 className={`text-3xl font-bold tracking-[-0.02em] sm:text-[2.6rem] sm:leading-[1.08] ${t.title}`}>{title}</h2>
      {intro && <p className={`mt-4 text-lg leading-relaxed ${t.intro}`}>{intro}</p>}
    </div>
  )
}
