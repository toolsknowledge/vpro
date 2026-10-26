import { Quote } from 'lucide-react'
import Container from './Container'
import SectionHeading from './SectionHeading'
import { stories } from '../data/site'

function Initials({ name }) {
  const initials = name.split(' ').map((n) => n[0]).join('')
  return (
    <span className="grid size-11 shrink-0 place-items-center rounded-full bg-brand-tint font-display text-sm font-bold text-[#9a4b00]">
      {initials}
    </span>
  )
}

export default function Stories() {
  const [featured, ...rest] = stories
  return (
    <section id="stories" className="py-20 lg:py-28">
      <Container>
        <SectionHeading title="What learners say after the course" />

        <div className="mt-12 grid gap-6 lg:grid-cols-[1.4fr_1fr]">
          <figure className="flex flex-col justify-between rounded-surface bg-brand-tint p-8 text-ink ring-1 ring-brand/25 sm:p-10">
            <Quote className="size-10 fill-brand text-brand" aria-hidden="true" />
            <blockquote className="mt-6 font-display text-2xl font-medium leading-snug tracking-[-0.01em] sm:text-[1.9rem]">
              {featured.quote}
            </blockquote>
            <figcaption className="mt-10 flex items-center gap-4">
              <span className="grid size-12 place-items-center rounded-full bg-brand font-display font-bold text-ink">
                {featured.name.split(' ').map((n) => n[0]).join('')}
              </span>
              <span>
                <span className="block font-semibold">{featured.name}</span>
                <span className="block text-sm text-ink-soft">{featured.role}, from {featured.course}</span>
              </span>
            </figcaption>
          </figure>

          <div className="grid gap-6">
            {rest.map((s) => (
              <figure key={s.name} className="rounded-surface bg-white p-7 ring-1 ring-line">
                <blockquote className="text-[17px] leading-relaxed text-ink-soft">{s.quote}</blockquote>
                <figcaption className="mt-6 flex items-center gap-3">
                  <Initials name={s.name} />
                  <span>
                    <span className="block font-semibold text-ink">{s.name}</span>
                    <span className="block text-sm text-slate">{s.role}</span>
                  </span>
                </figcaption>
              </figure>
            ))}
          </div>
        </div>
      </Container>
    </section>
  )
}
