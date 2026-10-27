import { useCallback, useEffect, useRef, useState } from 'react';
import { api } from '../api/client';

const POLL_INTERVAL_MS = 30000;

/** Health, indexing status, document list and sample questions, refreshed together. */
export function useBackendStatus() {
  const [state, setState] = useState({
    connection: 'checking', // checking | online | offline
    health: null,
    indexing: null,
    documents: null,
    sampleQuestions: null,
    error: null,
  });
  const controllerRef = useRef(null);

  const refresh = useCallback(async () => {
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    try {
      const [health, indexing, documents, sampleQuestions] = await Promise.all([
        api.health(controller.signal),
        api.indexingStatus(controller.signal),
        api.documents(controller.signal),
        api.sampleQuestions(controller.signal).catch(() => null),
      ]);
      setState({ connection: 'online', health, indexing, documents, sampleQuestions, error: null });
    } catch (error) {
      if (error.name === 'AbortError') return;
      setState((current) => ({ ...current, connection: 'offline', error: error.message }));
    }
  }, []);

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, POLL_INTERVAL_MS);
    return () => {
      clearInterval(timer);
      controllerRef.current?.abort();
    };
  }, [refresh]);

  return { ...state, refresh };
}
