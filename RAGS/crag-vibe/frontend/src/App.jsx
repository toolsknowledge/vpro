import { useCallback, useEffect, useRef, useState } from 'react'
import { askQuestion, fetchDocuments, fetchHealth, getErrorMessage, ingestDocuments } from './api'
import Header from './components/Header'
import WelcomeScreen from './components/WelcomeScreen'
import ChatInput from './components/ChatInput'
import WorkflowPanel from './components/WorkflowPanel'
import { AssistantMessage, ErrorMessage, TypingIndicator, UserMessage } from './components/ChatMessage'
import { TrashIcon } from './components/Icons'

const HEALTH_CHECK_INTERVAL_MS = 15000

export default function App() {
  const [backendStatus, setBackendStatus] = useState('checking')
  const [knowledgeBase, setKnowledgeBase] = useState(null)
  const [isIndexing, setIsIndexing] = useState(false)
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [pendingQuestion, setPendingQuestion] = useState('')
  const [selectedResponseId, setSelectedResponseId] = useState(null)
  const nextMessageId = useRef(1)
  const messagesRef = useRef(null)

  const addMessage = (message) => {
    const id = nextMessageId.current++
    setMessages((current) => [...current, { id, ...message }])
    return id
  }

  const loadKnowledgeBase = useCallback(() => {
    fetchDocuments()
      .then(setKnowledgeBase)
      .catch(() => setKnowledgeBase(null))
  }, [])

  // Check the backend now and every few seconds, so the status indicator stays accurate.
  useEffect(() => {
    const checkBackend = () =>
      fetchHealth()
        .then(() => setBackendStatus('online'))
        .catch(() => setBackendStatus('offline'))
    checkBackend()
    const timer = setInterval(checkBackend, HEALTH_CHECK_INTERVAL_MS)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    if (backendStatus === 'online') loadKnowledgeBase()
  }, [backendStatus, loadKnowledgeBase])

  // Auto-scroll inside the chat area only: to the start of a new answer, otherwise to the bottom.
  useEffect(() => {
    const container = messagesRef.current
    const latest = container?.lastElementChild
    if (!container || !latest || (messages.length === 0 && !isLoading)) return
    const showFromTop = latest.classList.contains('message-assistant') && latest.offsetHeight > container.clientHeight
    const top = showFromTop ? latest.offsetTop - 16 : container.scrollHeight
    container.scrollTo?.({ top, behavior: 'smooth' })
  }, [messages, isLoading])

  const sendQuestion = async (question) => {
    if (!question.trim() || isLoading) return
    addMessage({ role: 'user', text: question })
    setPendingQuestion(question)
    setIsLoading(true)
    try {
      const response = await askQuestion(question)
      setSelectedResponseId(addMessage({ role: 'assistant', response }))
      setBackendStatus('online')
    } catch (error) {
      addMessage({ role: 'error', text: getErrorMessage(error), question })
      if (!error.response) setBackendStatus('offline')
    } finally {
      setIsLoading(false)
    }
  }

  const handleIngest = async () => {
    setIsIndexing(true)
    try {
      await ingestDocuments()
    } catch (error) {
      addMessage({ role: 'error', text: getErrorMessage(error), question: null })
    } finally {
      setIsIndexing(false)
      loadKnowledgeBase()
    }
  }

  const clearConversation = () => {
    setMessages([])
    setSelectedResponseId(null)
  }

  const selectedResponse = messages.find((message) => message.id === selectedResponseId)?.response

  return (
    <div className="app">
      <Header backendStatus={backendStatus} />

      <main className="layout">
        <section className="chat-card" aria-label="Chat">
          <div className="chat-toolbar">
            <div>
              <h2>Student Chat</h2>
              <p>Answers come only from your PDF learning materials.</p>
            </div>
            <button
              type="button"
              className="btn btn-ghost"
              onClick={clearConversation}
              disabled={messages.length === 0 || isLoading}
            >
              <TrashIcon width={16} height={16} /> <span>Clear chat</span>
            </button>
          </div>

          <div className="messages" aria-live="polite" ref={messagesRef}>
            {messages.length === 0 && !isLoading ? (
              <WelcomeScreen
                onAsk={sendQuestion}
                disabled={isLoading}
                knowledgeBase={knowledgeBase}
                isIndexing={isIndexing}
                onIngest={handleIngest}
              />
            ) : (
              messages.map((message) => {
                if (message.role === 'user') return <UserMessage key={message.id} text={message.text} />
                if (message.role === 'error') {
                  return (
                    <ErrorMessage
                      key={message.id}
                      text={message.text}
                      disabled={isLoading}
                      onRetry={message.question ? () => sendQuestion(message.question) : undefined}
                    />
                  )
                }
                return (
                  <AssistantMessage
                    key={message.id}
                    response={message.response}
                    isSelected={message.id === selectedResponseId}
                    onSelect={() => setSelectedResponseId(message.id)}
                  />
                )
              })
            )}
            {isLoading && <TypingIndicator />}
          </div>

          <ChatInput onSend={sendQuestion} disabled={isLoading} />
        </section>

        <WorkflowPanel response={selectedResponse} isLoading={isLoading} pendingQuestion={pendingQuestion} />
      </main>
    </div>
  )
}
