import { useEffect, useRef } from 'react';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import LoadingIndicator from './LoadingIndicator';
import SampleQuestions from './SampleQuestions';

function Welcome({ sampleQuestions, onSelect }) {
  return (
    <div className="welcome">
      <h2>Welcome to the Adaptive RAG Assistant</h2>
      <p>
        Every question is routed before it is answered: <strong>DIRECT</strong> for general questions,{' '}
        <strong>RETRIEVE</strong> to answer from the indexed course documents, or <strong>CLARIFY</strong> when more
        detail is needed. The route and the reason are shown with each answer.
      </p>
      <SampleQuestions sampleQuestions={sampleQuestions} onSelect={onSelect} compact />
    </div>
  );
}

export default function ChatWindow({ chat, sampleQuestions, offline, draft, onDraftConsumed }) {
  const { messages, pending, send, retry } = chat;
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages.length, pending]);

  return (
    <section className="chat-window" aria-label="Conversation">
      <div className="chat-scroll">
        {messages.length === 0 ? (
          <Welcome sampleQuestions={sampleQuestions} onSelect={send} />
        ) : (
          <div className="message-list" aria-live="polite">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} onRetry={retry} retryDisabled={pending} />
            ))}
          </div>
        )}
        {pending && <LoadingIndicator />}
        <div ref={endRef} />
      </div>
      <ChatInput
        onSend={send}
        pending={pending}
        disabled={offline}
        draft={draft}
        onDraftConsumed={onDraftConsumed}
      />
    </section>
  );
}
