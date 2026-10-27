import { useEffect, useRef, useState } from 'react';
import { SendHorizontal } from 'lucide-react';

const MAX_LENGTH = 2000;

export default function ChatInput({ onSend, pending, disabled, draft, onDraftConsumed }) {
  const [value, setValue] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (draft) {
      setValue(draft);
      onDraftConsumed();
      textareaRef.current?.focus();
    }
  }, [draft, onDraftConsumed]);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 180)}px`;
  }, [value]);

  const canSend = value.trim().length > 0 && !pending && !disabled;

  const submit = (event) => {
    event.preventDefault();
    if (canSend && onSend(value)) setValue('');
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing) submit(event);
  };

  return (
    <form className="chat-input" onSubmit={submit}>
      <label htmlFor="chat-question" className="visually-hidden">
        Ask a question
      </label>
      <textarea
        id="chat-question"
        ref={textareaRef}
        value={value}
        onChange={(event) => setValue(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask about RAG, Adaptive RAG, ChromaDB… (Enter to send, Shift+Enter for a new line)"
        rows={1}
        maxLength={MAX_LENGTH}
        aria-describedby="chat-input-hint"
      />
      <button type="submit" className="button button--primary chat-input__send" disabled={!canSend} aria-label="Send">
        <SendHorizontal size={18} aria-hidden="true" />
        <span className="chat-input__send-label">Send</span>
      </button>
      <p id="chat-input-hint" className="chat-input__hint">
        {disabled ? 'Backend offline — start the API server to chat.' : `${value.length}/${MAX_LENGTH}`}
      </p>
    </form>
  );
}
