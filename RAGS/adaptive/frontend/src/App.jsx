import { useCallback, useEffect, useState } from 'react';
import ChatWindow from './components/ChatWindow';
import DocumentsPanel from './components/DocumentsPanel';
import Header from './components/Header';
import IndexingPanel from './components/IndexingPanel';
import OverviewPanel from './components/OverviewPanel';
import SampleQuestions from './components/SampleQuestions';
import Sidebar from './components/Sidebar';
import { useBackendStatus } from './hooks/useBackendStatus';
import { useChat } from './hooks/useChat';

export default function App() {
  const status = useBackendStatus();
  const chat = useChat();
  const [view, setView] = useState('chat');
  const [menuOpen, setMenuOpen] = useState(false);
  const [draft, setDraft] = useState('');

  const navigate = useCallback((nextView) => {
    setView(nextView);
    setMenuOpen(false);
  }, []);

  const startNewChat = useCallback(() => {
    chat.newChat();
    navigate('chat');
  }, [chat, navigate]);

  const askSample = useCallback(
    (question) => {
      navigate('chat');
      // If a request is still running, put the question in the input instead of dropping it.
      if (!chat.send(question)) setDraft(question);
    },
    [chat, navigate],
  );

  const clearDraft = useCallback(() => setDraft(''), []);

  useEffect(() => {
    if (!menuOpen) return undefined;
    const onKeyDown = (event) => event.key === 'Escape' && setMenuOpen(false);
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [menuOpen]);

  const offline = status.connection === 'offline';

  return (
    <div className="app">
      <Header
        connection={status.connection}
        health={status.health}
        indexing={status.indexing}
        menuOpen={menuOpen}
        onToggleMenu={() => setMenuOpen((open) => !open)}
      />
      {offline && (
        <div className="banner banner--danger" role="alert">
          {status.error} Start it with <code>bash start.sh</code> or see the README.
        </div>
      )}
      {!offline && status.health && !status.health.openai_configured && (
        <div className="banner banner--warning" role="status">
          OpenAI API key is not configured. The interface works, but chat and indexing need{' '}
          <code>OPENAI_API_KEY</code> in <code>backend/.env</code> (then restart the backend).
        </div>
      )}
      <div className="app-body">
        <Sidebar activeView={view} onNavigate={navigate} onNewChat={startNewChat} open={menuOpen} />
        {menuOpen && <button type="button" className="sidebar-backdrop" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}
        <main className="app-main">
          {view === 'chat' && (
            <ChatWindow
              chat={chat}
              sampleQuestions={status.sampleQuestions}
              offline={offline}
              draft={draft}
              onDraftConsumed={clearDraft}
            />
          )}
          {view === 'overview' && (
            <OverviewPanel connection={status.connection} health={status.health} indexing={status.indexing} />
          )}
          {view === 'samples' && (
            <div className="panel">
              <header className="panel__header">
                <h2>Sample Questions</h2>
                <p>Click a question to ask it. CLARIFY examples work best at the start of a new chat.</p>
              </header>
              <SampleQuestions sampleQuestions={status.sampleQuestions} onSelect={askSample} />
            </div>
          )}
          {view === 'documents' && (
            <DocumentsPanel documents={status.documents} onRefresh={status.refresh} connection={status.connection} />
          )}
          {view === 'indexing' && (
            <IndexingPanel
              indexing={status.indexing}
              health={status.health}
              connection={status.connection}
              onIndexed={status.refresh}
            />
          )}
        </main>
      </div>
    </div>
  );
}
