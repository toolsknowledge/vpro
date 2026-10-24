import { useEffect, useState } from 'react'
import { Menu, X, Phone } from 'lucide-react'
import Container from './Container'
import Logo from './Logo'
import Button from './Button'
import { navLinks } from '../data/site'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && setOpen(false)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  return (
    <header
      className={`sticky top-0 z-50 transition-[background-color,box-shadow] duration-300 ${
        scrolled || open ? 'bg-paper/90 shadow-[0_1px_0_var(--color-line)] backdrop-blur-md' : 'bg-transparent'
      }`}
    >
      <Container className="flex h-18 items-center justify-between gap-6">
        <Logo />

        <nav aria-label="Main" className="hidden lg:block">
          <ul className="flex items-center gap-1">
            {navLinks.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  className="rounded-lg px-3.5 py-2 text-[15px] font-medium text-slate transition-colors hover:bg-ink/5 hover:text-ink"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div className="hidden items-center gap-3 lg:flex">
          <a href="tel:+919000000000" className="flex items-center gap-2 text-sm font-medium text-slate hover:text-ink">
            <Phone className="size-4" aria-hidden="true" />
            Call a counsellor
          </a>
          <Button href="#demo" size="sm">Book a free demo</Button>
        </div>

        <button
          type="button"
          className="grid size-10 place-items-center rounded-lg text-ink hover:bg-ink/5 lg:hidden"
          aria-expanded={open}
          aria-controls="mobile-menu"
          aria-label={open ? 'Close menu' : 'Open menu'}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X className="size-6" /> : <Menu className="size-6" />}
        </button>
      </Container>

      <div
        id="mobile-menu"
        className={`grid transition-[grid-template-rows] duration-300 ease-out lg:hidden ${open ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'}`}
      >
        <div className="overflow-hidden">
          <Container className="flex flex-col gap-1 pb-6 pt-2">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                tabIndex={open ? 0 : -1}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-3 text-lg font-medium text-ink hover:bg-ink/5"
              >
                {link.label}
              </a>
            ))}
            <Button href="#demo" className="mt-3" tabIndex={open ? 0 : -1} onClick={() => setOpen(false)}>
              Book a free demo
            </Button>
          </Container>
        </div>
      </div>
    </header>
  )
}
