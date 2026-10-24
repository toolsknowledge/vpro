import { useState } from 'react'
import Panel from '../components/ui/Panel.jsx'
import FilterTabs from '../components/ui/FilterTabs.jsx'
import { AnnouncementItem } from '../components/dashboard/Announcements.jsx'
import { announcements } from '../data/announcements.js'

const categories = ['All', ...new Set(announcements.map((a) => a.category))]

export default function AnnouncementsView() {
  const [category, setCategory] = useState('All')
  const items = announcements.filter((a) => category === 'All' || a.category === category)

  return (
    <Panel
      title="Institute announcements"
      description="Newest first"
      action={
        <FilterTabs
          label="Filter by category"
          value={category}
          onChange={setCategory}
          options={categories.map((c) => ({ value: c, label: c }))}
        />
      }
    >
      <div className="max-w-3xl divide-y divide-line">
        {items.map((a) => (
          <AnnouncementItem key={a.id} item={a} />
        ))}
      </div>
    </Panel>
  )
}
