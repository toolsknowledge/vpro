import { Clock, MonitorPlay, CalendarDays, Check, Gauge } from 'lucide-react'
import Button from './Button'
import TrackChip from './TrackChip'
import { tracks } from '../data/site'

const inr = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 })

export default function CourseCard({ course }) {
  const { title, track, icon: Icon, level, weeks, mode, nextBatch, seatsLeft, fee, modules } = course
  const lowSeats = seatsLeft <= 6

  return (
    <article className="group relative flex flex-col rounded-2xl bg-white shadow-card ring-1 ring-line transition duration-300 ease-out hover:-translate-y-1 hover:shadow-lift hover:ring-ink/15">
      <div className={`h-1.5 rounded-t-2xl ${tracks[track].bar}`} aria-hidden="true" />
      <div className="flex flex-1 flex-col p-6">
        <div className="flex items-start justify-between gap-4">
          <span className="grid size-12 place-items-center rounded-xl bg-paper text-ink ring-1 ring-line transition-colors duration-300 group-hover:bg-ink group-hover:text-white">
            <Icon className="size-6" strokeWidth={1.75} aria-hidden="true" />
          </span>
          <TrackChip track={track} />
        </div>

        <h3 className="mt-5 text-xl font-bold leading-snug tracking-[-0.01em] text-ink">{title}</h3>

        <dl className="mt-3 flex flex-wrap gap-x-4 gap-y-1.5 text-sm text-slate">
          <div className="flex items-center gap-1.5">
            <dt className="sr-only">Duration</dt>
            <Clock className="size-4" aria-hidden="true" />
            <dd>{weeks} weeks</dd>
          </div>
          <div className="flex items-center gap-1.5">
            <dt className="sr-only">Format</dt>
            <MonitorPlay className="size-4" aria-hidden="true" />
            <dd>{mode}</dd>
          </div>
          <div className="flex items-center gap-1.5">
            <dt className="sr-only">Level</dt>
            <Gauge className="size-4" aria-hidden="true" />
            <dd>{level}</dd>
          </div>
        </dl>

        <ul className="mt-5 space-y-2 border-t border-line pt-5">
          {modules.map((m) => (
            <li key={m} className="flex items-center gap-2.5 text-[15px] text-ink-soft">
              <Check className="size-4 shrink-0 text-mint" strokeWidth={2.5} aria-hidden="true" />
              {m}
            </li>
          ))}
        </ul>

        <div className="mt-auto pt-6">
          <div className="flex items-center justify-between rounded-xl bg-paper px-4 py-3">
            <div className="flex items-center gap-2 text-sm">
              <CalendarDays className="size-4 text-slate" aria-hidden="true" />
              <span className="text-slate">Next batch</span>
              <span className="font-semibold text-ink">{nextBatch}</span>
            </div>
            <span className={`text-xs font-semibold ${lowSeats ? 'text-rose' : 'text-slate'}`}>
              {seatsLeft} seats left
            </span>
          </div>
          <div className="mt-4 flex items-center justify-between gap-4">
            <p>
              <span className="font-display text-2xl font-bold text-ink">{inr.format(fee)}</span>
              <span className="block text-xs text-slate">{fee > 15000 ? 'or 3 monthly instalments' : 'One-time payment'}</span>
            </p>
            <Button href="#demo" variant="dark" size="sm" aria-label={`View syllabus for ${title}`}>
              View syllabus
            </Button>
          </div>
        </div>
      </div>
    </article>
  )
}
