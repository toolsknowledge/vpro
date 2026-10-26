import { Star, Users, BadgeCheck } from 'lucide-react'
import Container from './Container'
import Button from './Button'
import Timetable from './Timetable'

const proof = [
  { icon: Star, text: '4.8 from 2,300+ learners' },
  { icon: Users, text: 'Batches capped at 30' },
  { icon: BadgeCheck, text: 'Mentors from product teams' },
]

export default function Hero() {
  return (
    <section id="top" className="relative overflow-hidden pb-20 pt-10 sm:pt-14 lg:pb-28 lg:pt-20">
      <Container className="grid items-center gap-12 lg:grid-cols-[1.05fr_1fr] lg:gap-16">
        <div>
          <p className="mb-6 inline-flex items-center gap-2 rounded-full bg-white px-3 py-1.5 text-sm font-medium text-slate ring-1 ring-line">
            <span className="size-2 rounded-full bg-brand" aria-hidden="true" />
            New React batch starts 2 November
          </p>
          <h1 className="text-[2.6rem] font-extrabold leading-[1.02] tracking-[-0.035em] text-ink sm:text-6xl lg:text-[4.4rem]">
            Learn to code in a live classroom, not a video playlist.
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-slate sm:text-xl">
            Mentor-led courses in React, Full Stack, Java, Python and AI-assisted development. You write code every
            class, get it reviewed, and leave with projects you can show.
          </p>
          <div className="mt-9 flex flex-col gap-3 sm:flex-row">
            <Button href="#courses" size="lg">Explore courses</Button>
            <Button href="#demo" variant="secondary" size="lg">Book a free demo class</Button>
          </div>
          <ul className="mt-10 flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:gap-x-5">
            {proof.map(({ icon: Icon, text }) => (
              <li key={text} className="flex items-center gap-2 text-sm font-medium text-ink-soft">
                <Icon className="size-4 text-brand-deep" aria-hidden="true" />
                {text}
              </li>
            ))}
          </ul>
        </div>

        <div className="relative">
          <div
            className="absolute -inset-8 -z-10 rounded-[40px] opacity-70 [mask-image:radial-gradient(closest-side,black,transparent)]"
            style={{
              backgroundImage:
                'linear-gradient(var(--color-line) 1px, transparent 1px), linear-gradient(90deg, var(--color-line) 1px, transparent 1px)',
              backgroundSize: '28px 28px',
            }}
            aria-hidden="true"
          />
          <Timetable />
        </div>
      </Container>
    </section>
  )
}
