import { useEffect } from 'react'
import { PanelLeftClose, PanelLeftOpen, X } from 'lucide-react'
import logo from '../../assets/logo.jpeg'
import { navItems, secondaryNavItems } from '../../data/navigation.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

function NavLink({ item, active, collapsed, badge, onSelect }) {
  const Icon = item.icon
  return (
    <li>
      <a
        href={`#/${item.id}`}
        onClick={(e) => {
          e.preventDefault()
          onSelect(item.id)
        }}
        aria-current={active ? 'page' : undefined}
        title={collapsed ? item.label : undefined}
        className={`group relative flex h-10 items-center gap-3 rounded-lg px-3 text-sm font-medium transition-colors ${
          active ? 'bg-navy-900 text-white' : 'text-ink-2 hover:bg-navy-50 hover:text-navy-900'
        } ${collapsed ? 'lg:justify-center lg:px-0' : ''}`}
      >
        <Icon className={`size-[18px] shrink-0 ${active ? 'text-brand' : 'text-ink-3 group-hover:text-navy-700'}`} aria-hidden="true" />
        <span className={collapsed ? 'lg:sr-only' : ''}>{item.label}</span>
        {badge > 0 && (
          <span
            className={`tabular ml-auto rounded-md px-1.5 text-[11px] font-bold ${active ? 'bg-white/15 text-white' : 'bg-bad-bg text-bad'} ${
              collapsed ? 'lg:absolute lg:top-1 lg:right-1.5 lg:ml-0 lg:size-2 lg:rounded-full lg:bg-bad lg:p-0 lg:text-[0px]' : ''
            }`}
          >
            {badge}
            <span className="sr-only"> overdue</span>
          </span>
        )}
      </a>
    </li>
  )
}

export default function Sidebar({ view, onNavigate, collapsed, onToggleCollapsed, mobileOpen, onCloseMobile }) {
  const { assignments } = useDashboard()
  const overdue = assignments.filter((a) => a.status === 'overdue').length
  const badges = { assignments: overdue }

  useEffect(() => {
    if (!mobileOpen) return
    const onKey = (e) => e.key === 'Escape' && onCloseMobile()
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [mobileOpen, onCloseMobile])

  const select = (id) => {
    onNavigate(id)
    onCloseMobile()
  }

  return (
    <>
      {mobileOpen && <div className="fixed inset-0 z-30 bg-navy-950/40 lg:hidden" onClick={onCloseMobile} aria-hidden="true" />}
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-line bg-white transition-[transform,width] duration-200 lg:sticky lg:top-0 lg:z-auto lg:h-dvh lg:translate-x-0 ${
          mobileOpen ? 'translate-x-0 shadow-pop' : '-translate-x-full'
        } ${collapsed ? 'lg:w-[76px]' : 'lg:w-64'}`}
        aria-label="Main navigation"
      >
        <div className={`flex h-16 shrink-0 items-center justify-between border-b border-line px-4 ${collapsed ? 'lg:justify-center lg:px-2' : ''}`}>
          <a
            href="#/dashboard"
            onClick={(e) => {
              e.preventDefault()
              select('dashboard')
            }}
            className="block"
            aria-label="VPRO Skills EDUTECH, go to dashboard"
          >
            {/* Collapsed: crop to the hand mark on the left of the logo. */}
            <span className={`block overflow-hidden ${collapsed ? 'lg:w-[30px]' : ''}`}>
              <img src={logo} alt="" width="80" height="55" className="h-[55px] w-[80px] max-w-none object-cover object-left" />
            </span>
          </a>
          <button type="button" onClick={onCloseMobile} className="rounded-lg p-2 text-ink-3 hover:bg-navy-50 lg:hidden" aria-label="Close menu">
            <X className="size-5" aria-hidden="true" />
          </button>
        </div>

        <nav className="flex flex-1 flex-col overflow-y-auto px-3 pt-4 pb-2">
          <ul className="space-y-1">
            {navItems.map((item) => (
              <NavLink key={item.id} item={item} active={view === item.id} collapsed={collapsed} badge={badges[item.id]} onSelect={select} />
            ))}
          </ul>
          <ul className="mt-auto space-y-1 border-t border-line pt-3">
            {secondaryNavItems.map((item) => (
              <NavLink key={item.id} item={item} active={view === item.id} collapsed={collapsed} onSelect={select} />
            ))}
          </ul>
        </nav>

        <div className="hidden shrink-0 px-3 pb-4 lg:block">
          <button
            type="button"
            onClick={onToggleCollapsed}
            aria-expanded={!collapsed}
            className={`flex h-10 w-full items-center gap-3 rounded-lg px-3 text-sm font-medium text-ink-3 hover:bg-navy-50 hover:text-navy-900 ${
              collapsed ? 'justify-center px-0' : ''
            }`}
            title={collapsed ? 'Expand sidebar' : undefined}
          >
            {collapsed ? <PanelLeftOpen className="size-[18px]" aria-hidden="true" /> : <PanelLeftClose className="size-[18px]" aria-hidden="true" />}
            <span className={collapsed ? 'sr-only' : ''}>{collapsed ? 'Expand sidebar' : 'Collapse sidebar'}</span>
          </button>
        </div>
      </aside>
    </>
  )
}
