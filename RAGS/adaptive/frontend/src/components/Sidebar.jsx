import { Database, FileText, LayoutDashboard, Lightbulb, MessageSquarePlus, MessagesSquare } from 'lucide-react';

export const VIEWS = [
  { id: 'chat', label: 'Chat', icon: MessagesSquare },
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'samples', label: 'Sample Questions', icon: Lightbulb },
  { id: 'documents', label: 'Indexed Documents', icon: FileText },
  { id: 'indexing', label: 'Indexing Controls', icon: Database },
];

export default function Sidebar({ activeView, onNavigate, onNewChat, open }) {
  return (
    <nav id="app-sidebar" className={`sidebar${open ? ' sidebar--open' : ''}`} aria-label="Main navigation">
      <button type="button" className="button button--primary sidebar-new-chat" onClick={onNewChat} title="New chat">
        <MessageSquarePlus size={18} aria-hidden="true" />
        <span className="sidebar-label">New Chat</span>
      </button>
      <ul className="sidebar-nav">
        {VIEWS.map(({ id, label, icon: Icon }) => (
          <li key={id}>
            <button
              type="button"
              className={`sidebar-link${activeView === id ? ' sidebar-link--active' : ''}`}
              aria-current={activeView === id ? 'page' : undefined}
              onClick={() => onNavigate(id)}
              title={label}
            >
              <Icon size={18} aria-hidden="true" />
              <span className="sidebar-label">{label}</span>
            </button>
          </li>
        ))}
      </ul>
      <p className="sidebar-footer sidebar-label">VPRO Skills EduTech · Adaptive RAG</p>
    </nav>
  );
}
