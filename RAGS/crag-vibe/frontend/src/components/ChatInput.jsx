import { useState } from 'react'
import { SendIcon } from './Icons'

const MAX_QUESTION_LENGTH = 500

export default function ChatInput({ onSend, disabled }) {
  const [question, setQuestion] = useState('')
  const canSend = question.trim().length > 0 && !disabled

  const submit = () => {
    if (!canSend) return
    onSend(question.trim())
    setQuestion('')
  }

  return (
    <form
      className="chat-input"
      onSubmit={(event) => {
        event.preventDefault()
        submit()
      }}
    >
      <div className="input-wrapper">
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault()
              submit()
            }
          }}
          placeholder="Ask a question about your Python learning materials…"
          aria-label="Your question"
          maxLength={MAX_QUESTION_LENGTH}
          rows={1}
        />
        <button type="submit" className="send-button" disabled={!canSend} aria-label="Send question">
          <SendIcon />
        </button>
      </div>
      <div className="input-hint">
        <span>Press Enter to send · Shift + Enter for a new line</span>
        <span>{question.length}/{MAX_QUESTION_LENGTH}</span>
      </div>
    </form>
  )
}
