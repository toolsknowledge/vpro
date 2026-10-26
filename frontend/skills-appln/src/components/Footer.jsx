import { Mail, MapPin, Phone } from 'lucide-react'
import Container from './Container'
import Logo from './Logo'
import { courses, navLinks } from '../data/site'

const company = ['About us', 'Mentors', 'Hiring partners', 'Careers']

function Column({ title, children }) {
  return (
    <div>
      <h3 className="font-sans text-sm font-semibold text-white">{title}</h3>
      <ul className="mt-4 space-y-3 text-[15px]">{children}</ul>
    </div>
  )
}

const year = new Date().getFullYear()
const linkClass = 'text-white/60 transition-colors hover:text-white'

export default function Footer() {
  return (
    <footer className="bg-ink text-white">
      <Container className="grid gap-12 py-16 md:grid-cols-2 lg:grid-cols-[1.5fr_1fr_1fr_1.2fr]">
        <div className="max-w-xs">
          <Logo onDark />
          <p className="mt-5 leading-relaxed text-white/60">
            Live, mentor-led software training for students and working professionals across India.
          </p>
        </div>

        <Column title="Courses">
          {courses.slice(0, 5).map((c) => (
            <li key={c.id}><a href="#courses" className={linkClass}>{c.title.split(':')[0].replace(' with Modern JavaScript', '')}</a></li>
          ))}
        </Column>

        <Column title="Company">
          {[...company, ...navLinks.slice(3).map((l) => l.label)].map((label) => (
            <li key={label}><a href={label === 'FAQ' ? '#faq' : '#top'} className={linkClass}>{label}</a></li>
          ))}
        </Column>

        <Column title="Talk to us">
          <li className="flex gap-3 text-white/60"><Phone className="mt-0.5 size-4 shrink-0" aria-hidden="true" /><a href="tel:+919000000000" className={linkClass}>+91 90000 00000</a></li>
          <li className="flex gap-3 text-white/60"><Mail className="mt-0.5 size-4 shrink-0" aria-hidden="true" /><a href="mailto:info@vproskills.com" className={linkClass}>info@vproskills.com</a></li>
          <li className="flex gap-3 text-white/60"><MapPin className="mt-0.5 size-4 shrink-0" aria-hidden="true" />Ameerpet, Hyderabad, Telangana</li>
        </Column>
      </Container>

      <div className="border-t border-white/10">
        <Container className="flex flex-col gap-3 py-6 text-sm text-white/50 sm:flex-row sm:items-center sm:justify-between">
          <p>© {year} VPro Skills EduTech. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="#top" className="hover:text-white">Privacy</a>
            <a href="#top" className="hover:text-white">Terms</a>
            <a href="#top" className="hover:text-white">Refund policy</a>
          </div>
        </Container>
      </div>
    </footer>
  )
}
