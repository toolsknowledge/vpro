import { ChevronDown } from 'lucide-react'
import Container from './Container'
import SectionHeading from './SectionHeading'
import { faqs } from '../data/site'

export default function Faq() {
  return (
    <section id="faq" className="border-t border-line py-20 lg:py-28">
      <Container className="grid gap-10 lg:grid-cols-[1fr_1.6fr] lg:gap-16">
        <SectionHeading
          title="Questions before you join"
          intro="Still unsure? A counsellor can walk you through the right course in a 15-minute call."
        />
        <div className="divide-y divide-line border-y border-line">
          {faqs.map((f) => (
            <details key={f.q} className="group py-1">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-6 rounded-lg py-5 text-left text-lg font-semibold text-ink [&::-webkit-details-marker]:hidden">
                {f.q}
                <ChevronDown className="size-5 shrink-0 text-slate transition-transform duration-300 group-open:rotate-180" aria-hidden="true" />
              </summary>
              <p className="max-w-2xl pb-6 leading-relaxed text-slate">{f.a}</p>
            </details>
          ))}
        </div>
      </Container>
    </section>
  )
}
