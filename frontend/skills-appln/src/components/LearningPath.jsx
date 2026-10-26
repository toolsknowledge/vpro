import Container from './Container'
import SectionHeading from './SectionHeading'
import { pathSteps } from '../data/site'

export default function LearningPath() {
  return (
    <section id="path" className="bg-ink py-20 text-white lg:py-28">
      <Container>
        <SectionHeading
          tone="dark"
          title="From first class to first interview"
          intro="The same four stages for every course, so you always know what comes next."
        />

        <ol className="relative mt-14 grid gap-10 md:grid-cols-2 lg:grid-cols-4 lg:gap-8">
          <span className="absolute left-0 right-0 top-5 hidden h-px bg-white/15 lg:block" aria-hidden="true" />
          {pathSteps.map((step, i) => (
            <li key={step.title} className="relative">
              <span className="relative grid size-10 place-items-center rounded-full bg-brand font-display text-base font-bold text-ink ring-8 ring-ink">
                {i + 1}
              </span>
              <h3 className="mt-6 text-xl font-semibold">{step.title}</h3>
              <p className="mt-2 leading-relaxed text-white/65">{step.body}</p>
            </li>
          ))}
        </ol>
      </Container>
    </section>
  )
}
