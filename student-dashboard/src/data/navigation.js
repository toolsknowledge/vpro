import {
  Award,
  BookOpen,
  CalendarCheck,
  ClipboardList,
  FolderKanban,
  LayoutDashboard,
  LifeBuoy,
  Megaphone,
  Settings,
  TrendingUp,
} from 'lucide-react'

export const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'courses', label: 'My Courses', icon: BookOpen },
  { id: 'learning', label: 'My Learning', icon: TrendingUp },
  { id: 'attendance', label: 'Attendance', icon: CalendarCheck },
  { id: 'assignments', label: 'Assignments', icon: ClipboardList },
  { id: 'projects', label: 'Projects', icon: FolderKanban },
  { id: 'certificates', label: 'Certificates', icon: Award },
  { id: 'announcements', label: 'Announcements', icon: Megaphone },
]

export const secondaryNavItems = [
  { id: 'support', label: 'Help & Support', icon: LifeBuoy },
  { id: 'settings', label: 'Settings', icon: Settings },
]

export const allNavItems = [...navItems, ...secondaryNavItems]
