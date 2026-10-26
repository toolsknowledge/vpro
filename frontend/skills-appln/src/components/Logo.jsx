import logo from '../assets/vpro-logo.png'

// The logo has charcoal artwork, so on dark backgrounds it sits on a white plate.
export default function Logo({ onDark = false }) {
  const img = <img src={logo} alt="VPro Skills" width="217" height="108" className="h-10 w-auto sm:h-11" />
  return (
    <a href="#top" className="inline-flex shrink-0" aria-label="VPro Skills home">
      {onDark ? <span className="rounded-xl bg-white px-3 py-2">{img}</span> : img}
    </a>
  )
}
