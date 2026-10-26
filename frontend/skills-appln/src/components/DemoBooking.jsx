import { useState } from 'react'
import { CalendarCheck, CircleCheck } from 'lucide-react'
import Container from './Container'
import Button from './Button'
import SectionHeading from './SectionHeading'
import { courses } from '../data/site'

const fieldClass =
  'h-12 w-full rounded-xl bg-white px-4 text-[15px] text-ink ring-1 ring-line placeholder:text-slate/60 transition focus:outline-none focus:ring-2 focus:ring-ink'

export default function DemoBooking() {
  const [form, setForm] = useState({ name: '', phone: '', course: courses[0].id })
  const [error, setError] = useState('')
  const [booked, setBooked] = useState(null)

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }))

  const submit = (e) => {
    e.preventDefault()
    if (!form.name.trim()) return setError('Enter your name so the mentor knows who is joining.')
    if (!/^[6-9]\d{9}$/.test(form.phone.replace(/\D/g, '').slice(-10))) {
      return setError('Enter a 10-digit mobile number. We send the class link there on WhatsApp.')
    }
    setError('')
    setBooked(courses.find((c) => c.id === form.course))
  }

  return (
    <section id="demo" className="pb-20 lg:pb-28">
      <Container>
        <div className="grid overflow-hidden rounded-surface bg-brand lg:grid-cols-2">
          <div className="p-8 sm:p-12">
            <CalendarCheck className="size-9 text-ink" strokeWidth={1.75} aria-hidden="true" />
            <SectionHeading
              tone="brand"
              className="mt-6"
              title="Sit in on a real class this Saturday"
              intro="Free, live and 90 minutes long. You will code along with the batch and can ask the mentor anything."
            />
          </div>

          <div className="bg-white p-8 sm:p-12">
            {booked ? (
              <div role="status" className="flex h-full flex-col justify-center">
                <CircleCheck className="size-10 text-mint" aria-hidden="true" />
                <p className="mt-4 font-display text-2xl font-bold text-ink">Demo class booked</p>
                <p className="mt-2 leading-relaxed text-slate">
                  Thanks, {form.name.split(' ')[0]}. We will send the joining link for {booked.title} to your WhatsApp
                  before Saturday, 8 AM.
                </p>
                <button
                  type="button"
                  onClick={() => setBooked(null)}
                  className="mt-6 self-start text-sm font-semibold text-ink underline-offset-4 hover:underline"
                >
                  Book for another course
                </button>
              </div>
            ) : (
              <form onSubmit={submit} noValidate className="grid gap-4">
                <label className="grid gap-1.5">
                  <span className="text-sm font-semibold text-ink">Full name</span>
                  <input className={fieldClass} value={form.name} onChange={update('name')} autoComplete="name" placeholder="Your name" />
                </label>
                <label className="grid gap-1.5">
                  <span className="text-sm font-semibold text-ink">WhatsApp number</span>
                  <input
                    className={fieldClass}
                    value={form.phone}
                    onChange={update('phone')}
                    inputMode="tel"
                    autoComplete="tel"
                    placeholder="98765 43210"
                  />
                </label>
                <label className="grid gap-1.5">
                  <span className="text-sm font-semibold text-ink">Course</span>
                  <select className={fieldClass} value={form.course} onChange={update('course')}>
                    {courses.map((c) => (
                      <option key={c.id} value={c.id}>{c.title}</option>
                    ))}
                  </select>
                </label>
                {error && <p role="alert" className="text-sm font-medium text-[#a72649]">{error}</p>}
                <Button as="button" type="submit" variant="dark" size="lg" className="mt-2">Book my demo class</Button>
              </form>
            )}
          </div>
        </div>
      </Container>
    </section>
  )
}
