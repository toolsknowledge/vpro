import { useState } from 'react'
import { weekdays } from '../../data/learning.js'
import { formatMinutes } from '../../lib/format.js'

const AXIS_MAX = 180 // minutes; gridlines every hour

// Single-series bar chart of daily learning minutes. Today's bar is marked in brand orange.
export default function WeeklyActivityChart({ minutes, highlightIndex }) {
  const [hover, setHover] = useState(null)
  const ticks = [180, 120, 60, 0]

  return (
    <figure className="m-0">
      <div className="relative flex h-52 gap-3">
        <div className="flex w-7 flex-col justify-between pb-6 text-right text-xs text-ink-3 tabular" aria-hidden="true">
          {ticks.map((t) => (
            <span key={t} className="-translate-y-1/2 leading-none first:translate-y-0 last:translate-y-0">
              {t / 60}h
            </span>
          ))}
        </div>
        <div className="relative flex-1">
          <div className="absolute inset-x-0 top-0 bottom-6 flex flex-col justify-between" aria-hidden="true">
            {ticks.map((t) => (
              <span key={t} className={`border-t ${t === 0 ? 'border-navy-300' : 'border-dashed border-line'}`} />
            ))}
          </div>
          <div className="absolute inset-0 grid grid-cols-7 gap-2">
            {minutes.map((m, i) => {
              const isToday = i === highlightIndex
              const height = Math.max((m / AXIS_MAX) * 100, m ? 3 : 0)
              return (
                <div key={weekdays[i]} className="flex flex-col">
                  <div
                    className="relative flex flex-1 items-end justify-center"
                    tabIndex={0}
                    role="img"
                    aria-label={`${weekdays[i]}: ${m ? formatMinutes(m) : 'no learning'}`}
                    onMouseEnter={() => setHover(i)}
                    onMouseLeave={() => setHover(null)}
                    onFocus={() => setHover(i)}
                    onBlur={() => setHover(null)}
                  >
                    <div
                      className={`w-full max-w-10 rounded-t transition-colors ${isToday ? 'bg-brand' : hover === i ? 'bg-navy-900' : 'bg-navy-700'}`}
                      style={{ height: `${height}%` }}
                    />
                    {hover === i && (
                      <div className="pointer-events-none absolute z-10 rounded-md bg-navy-950 px-2 py-1 text-xs whitespace-nowrap text-white shadow-pop" style={{ bottom: `calc(${height}% + 6px)` }}>
                        <span className="font-semibold">{weekdays[i]}</span> {m ? formatMinutes(m) : 'No learning'}
                      </div>
                    )}
                  </div>
                  <span className={`mt-1.5 h-[18px] text-center text-xs ${isToday ? 'font-semibold text-ink' : 'text-ink-3'}`}>
                    {isToday ? 'Today' : weekdays[i]}
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      </div>
      <table className="sr-only">
        <caption>Learning minutes per day</caption>
        <tbody>
          {minutes.map((m, i) => (
            <tr key={weekdays[i]}>
              <th scope="row">{weekdays[i]}</th>
              <td>{m} minutes</td>
            </tr>
          ))}
        </tbody>
      </table>
    </figure>
  )
}
