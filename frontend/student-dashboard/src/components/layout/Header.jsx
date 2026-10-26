import { useState } from 'react'
import { Menu, Search, X } from 'lucide-react'
import SearchBox from './SearchBox.jsx'
import NotificationPanel from './NotificationPanel.jsx'
import ProfileMenu from './ProfileMenu.jsx'

export default function Header({ title, subtitle, onOpenMobileNav, onNavigate }) {
  const [mobileSearch, setMobileSearch] = useState(false)

  return (
    <header className="sticky top-0 z-20 border-b border-line bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/85">
      <div className="flex h-16 items-center gap-3 px-4 sm:px-6 lg:px-8">
        <button type="button" onClick={onOpenMobileNav} className="-ml-1 rounded-lg p-2 text-ink-2 hover:bg-navy-50 lg:hidden" aria-label="Open menu">
          <Menu className="size-5" aria-hidden="true" />
        </button>
        <div className="min-w-0 flex-1">
          <h1 className="truncate text-lg leading-tight font-bold sm:text-xl">{title}</h1>
          {subtitle && <p className="hidden truncate text-[13px] text-ink-3 lg:block">{subtitle}</p>}
        </div>
        <SearchBox onNavigate={onNavigate} className="hidden w-72 md:block xl:w-80" />
        <button
          type="button"
          onClick={() => setMobileSearch((s) => !s)}
          aria-expanded={mobileSearch}
          className="inline-flex size-10 items-center justify-center rounded-lg text-ink-2 hover:bg-navy-50 md:hidden"
          aria-label={mobileSearch ? 'Close search' : 'Search'}
        >
          {mobileSearch ? <X className="size-5" aria-hidden="true" /> : <Search className="size-5" aria-hidden="true" />}
        </button>
        <NotificationPanel onNavigate={onNavigate} />
        <ProfileMenu onNavigate={onNavigate} />
      </div>
      {mobileSearch && (
        <div className="border-t border-line px-4 py-3 md:hidden">
          <SearchBox onNavigate={onNavigate} autoFocus />
        </div>
      )}
    </header>
  )
}
