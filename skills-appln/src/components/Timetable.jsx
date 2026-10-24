import { Radio, Video } from 'lucide-react'
import Button from './Button'
import { week } from '../data/site'

const FIRST_HOUR = 7
const HOURS = 14
const axis = [0, 3, 6, 9, 12]

const slotStyles = {
  frontend: 'bg-cobalt text-white',
  fullstack: 'bg-brand text-ink',
  data: 'bg-mint text-white',
  cloud: 'bg-rose text-white',
}

function formatTime(offset) {
  const total = FIRST_HOUR + offset
  const h = Math.floor(total)
  const m = Math.round((total - h) * 60)
  const suffix = h >= 12 ? 'PM' : 'AM'
  const h12 = h % 12 === 0 ? 12 : h % 12
  return m ? `${h12}:${String(m).padStart(2, '0')} ${suffix}` : `${h12} ${suffix}`
}

// JS getDay(): 0 = Sunday. Our week starts on Monday.
const todayIndex = (new Date().getDay() + 6) % 7

export default function Timetable() {
  const live = week.flatMap((d) => d.slots.map((s) => ({ ...s, day: d.day }))).find((s) => s.live)

  return (
    <figure className="relative rounded-surface bg-white p-4 shadow-[0_30px_60px_-30px_rgb(35_36_40/0.35)] ring-1 ring-line sm:p-6">
      <figcaption className="flex items-start justify-between gap-4">
        <div>
          <p className="font-display text-lg font-semibold text-ink">A week in Batch 14</p>
          <p className="text-sm text-slate">Live classes in IST, recordings posted the same day</p>
        </div>
        <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full bg-mint-tint px-2.5 py-1 text-xs font-semibold text-[#0d6b55]">
          <span className="live-dot size-2 rounded-full bg-mint" aria-hidden="true" />
          Enrolling
        </span>
      </figcaption>

      {/* Calendar grid (tablet and up) */}
      <div className="mt-5 hidden grid-cols-[2.75rem_repeat(7,minmax(0,1fr))] gap-x-1.5 sm:grid">
        <div />
        {week.map((d, i) => (
          <div
            key={d.day}
            className={`pb-2 text-center text-xs font-semibold ${i === todayIndex ? 'text-ink' : 'text-slate'}`}
          >
            {d.day}
            {i === todayIndex && <span className="mx-auto mt-1 block h-0.5 w-4 rounded-full bg-brand" />}
          </div>
        ))}

        <div className="relative" style={{ height: HOURS * 28 }}>
          {axis.map((h) => (
            <span
              key={h}
              className="absolute right-1 -translate-y-1/2 text-[11px] font-medium text-slate/80"
              style={{ top: `${(h / HOURS) * 100}%` }}
            >
              {formatTime(h)}
            </span>
          ))}
        </div>

        {week.map((d, di) => (
          <div
            key={d.day}
            className={`relative rounded-lg ${di === todayIndex ? 'bg-brand-tint/70' : 'bg-paper'}`}
            style={{
              height: HOURS * 28,
              backgroundImage: 'linear-gradient(to bottom, var(--color-line) 1px, transparent 1px)',
              backgroundSize: `100% ${100 / (HOURS / 3)}%`,
            }}
          >
            {d.slots.map((s, si) => (
              <div
                key={s.title}
                title={`${d.day}, ${formatTime(s.start)}: ${s.title}`}
                className={`slot-in absolute inset-x-0.5 overflow-hidden rounded-md p-1 text-[11px] font-semibold leading-[1.15] ${slotStyles[s.track]} ${
                  s.live ? 'ring-2 ring-ink ring-offset-2 ring-offset-white' : ''
                }`}
                style={{
                  top: `${(s.start / HOURS) * 100}%`,
                  height: `${(s.length / HOURS) * 100}%`,
                  animationDelay: `${180 + di * 70 + si * 90}ms`,
                }}
              >
                {s.title}
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Agenda list (phones) */}
      <ul className="mt-4 divide-y divide-line sm:hidden">
        {week
          .filter((d) => d.slots.length)
          .map((d) =>
            d.slots.map((s, si) => (
              <li key={s.title} className="slot-in flex items-center gap-3 py-2.5" style={{ animationDelay: `${si * 60}ms` }}>
                <span className={`h-8 w-1.5 shrink-0 rounded-full ${slotStyles[s.track].split(' ')[0]}`} aria-hidden="true" />
                <span className="w-10 text-xs font-semibold text-slate">{d.day}</span>
                <span className="flex-1 text-sm font-medium text-ink">{s.title}</span>
                <span className="text-xs text-slate">{formatTime(s.start)}</span>
              </li>
            )),
          )}
      </ul>

      {live && (
        <div className="mt-5 flex flex-col gap-3 rounded-xl bg-ink p-4 text-white sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <span className="grid size-10 shrink-0 place-items-center rounded-lg bg-white/10">
              <Radio className="size-5 text-brand" aria-hidden="true" />
            </span>
            <div>
              <p className="text-sm font-semibold">{live.title.replace('Live: ', '')}</p>
              <p className="text-xs text-white/65">
                {live.day === 'Sat' ? 'Saturday' : live.day}, {formatTime(live.start)}. Open to demo students.
              </p>
            </div>
          </div>
          <Button href="#demo" size="sm">
            <Video className="size-4" aria-hidden="true" />
            Save my seat
          </Button>
        </div>
      )}
    </figure>
  )
}
