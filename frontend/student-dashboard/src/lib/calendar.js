// Builds an .ics file in the browser so a class can be added to any calendar app. Nothing is sent anywhere.
function icsStamp(value) {
  const d = new Date(value)
  return d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')
}

export function downloadClassIcs(cls, courseTitle) {
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//VPRO Skills//Student Dashboard Prototype//EN',
    'BEGIN:VEVENT',
    `UID:${cls.id}@student-dashboard.local`,
    `DTSTAMP:${icsStamp(Date.now())}`,
    `DTSTART:${icsStamp(cls.start)}`,
    `DTEND:${icsStamp(cls.end)}`,
    `SUMMARY:${cls.title} (${courseTitle})`,
    `DESCRIPTION:Trainer: ${cls.trainer}. ${cls.prepare}`,
    `LOCATION:${cls.mode}`,
    'END:VEVENT',
    'END:VCALENDAR',
  ]
  const blob = new Blob([lines.join('\r\n')], { type: 'text/calendar' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${cls.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.ics`
  a.click()
  URL.revokeObjectURL(url)
}
