import { useCallback, useEffect, useRef, useState } from 'react';
import { api } from '../api/client';
import { createSessionId } from '../utils/formatters';

let messageCounter = 0;
const nextMessageId = () => `m${++messageCounter}`;

/**
 * Conversation state for one chat session.
 * - Only one request may be in flight; extra sends are ignored.
 * - Each request carries a sequence number; responses from an aborted or
 *   superseded request (e.g. after "New chat") are discarded.
 */
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [pending, setPending] = useState(false);
  const sessionIdRef = useRef(createSessionId());
  const requestSeqRef = useRef(0);
  const controllerRef = useRef(null);
  const pendingRef = useRef(false);

  useEffect(() => () => controllerRef.current?.abort(), []);

  const ask = useCallback(async (question) => {
    const seq = ++requestSeqRef.current;
    const controller = new AbortController();
    controllerRef.current = controller;
    pendingRef.current = true;
    setPending(true);
    try {
      const response = await api.chat({ question, sessionId: sessionIdRef.current }, controller.signal);
      if (seq !== requestSeqRef.current) return;
      setMessages((current) => [
        ...current,
        { id: nextMessageId(), role: 'assistant', content: response.answer, response },
      ]);
    } catch (error) {
      if (error.name === 'AbortError' || seq !== requestSeqRef.current) return;
      setMessages((current) => [
        ...current,
        {
          id: nextMessageId(),
          role: 'error',
          content: error.message,
          question,
          retryable: error.retryable ?? true,
        },
      ]);
    } finally {
      if (seq === requestSeqRef.current) {
        pendingRef.current = false;
        setPending(false);
        controllerRef.current = null;
      }
    }
  }, []);

  const send = useCallback(
    (text) => {
      const question = text.trim();
      if (!question || pendingRef.current) return false;
      setMessages((current) => [...current, { id: nextMessageId(), role: 'user', content: question }]);
      ask(question);
      return true;
    },
    [ask],
  );

  const retry = useCallback(
    (errorMessageId) => {
      if (pendingRef.current) return;
      const failed = messages.find((message) => message.id === errorMessageId);
      if (!failed) return;
      setMessages((current) => current.filter((message) => message.id !== errorMessageId));
      ask(failed.question);
    },
    [ask, messages],
  );

  const newChat = useCallback(() => {
    controllerRef.current?.abort();
    requestSeqRef.current += 1; // invalidate anything still in flight
    pendingRef.current = false;
    setPending(false);
    const previousSession = sessionIdRef.current;
    sessionIdRef.current = createSessionId();
    setMessages([]);
    // Forgetting server-side history is best effort; a new session id already isolates the next chat.
    api.clearSession(previousSession).catch(() => {});
  }, []);

  return { messages, pending, send, retry, newChat };
}
