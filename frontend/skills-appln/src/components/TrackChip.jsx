import { tracks } from '../data/site'

export default function TrackChip({ track }) {
  const t = tracks[track]
  return <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-semibold ${t.chip}`}>{t.label}</span>
}
