import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from '../App'
import * as api from '../api'
import { correctedResponse, insufficientResponse, knowledgeBase, relevantResponse } from './fixtures'

vi.mock('../api', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual, // keep the real getErrorMessage
    fetchHealth: vi.fn(),
    fetchDocuments: vi.fn(),
    askQuestion: vi.fn(),
    ingestDocuments: vi.fn(),
  }
})

function deferred() {
  let resolve
  let reject
  const promise = new Promise((res, rej) => {
    resolve = res
    reject = rej
  })
  return { promise, resolve, reject }
}

const questionBox = () => screen.getByLabelText('Your question')
const sendButton = () => screen.getByRole('button', { name: 'Send question' })

beforeEach(() => {
  vi.clearAllMocks()
  api.fetchHealth.mockResolvedValue({ status: 'ok' })
  api.fetchDocuments.mockResolvedValue(knowledgeBase)
})

describe('App', () => {
  it('renders the header, logo, welcome screen and sample questions', async () => {
    render(<App />)

    expect(screen.getByAltText('VPro Skills EduTech')).toHaveAttribute('src', '/logo.jpeg')
    expect(screen.getByText('Corrective RAG Assistant')).toBeInTheDocument()
    expect(screen.getByText('Welcome to VPro Skills AI Learning Assistant')).toBeInTheDocument()
    expect(screen.getAllByRole('button', { name: /What is Python\?|Explain Python|List and Tuple|OOPS/ })).toHaveLength(5)
    expect(await screen.findByText('Backend connected')).toBeInTheDocument()
    expect(await screen.findByText(/25 chunks indexed/)).toBeInTheDocument()
  })

  it('shows the backend as offline when the health check fails', async () => {
    api.fetchHealth.mockRejectedValue(new Error('Network Error'))
    render(<App />)

    expect(await screen.findByText('Backend offline')).toBeInTheDocument()
  })

  it('disables the send button until a question is typed', () => {
    render(<App />)

    expect(sendButton()).toBeDisabled()
    fireEvent.change(questionBox(), { target: { value: '   ' } })
    expect(sendButton()).toBeDisabled()
    fireEvent.change(questionBox(), { target: { value: 'What is a tuple?' } })
    expect(sendButton()).toBeEnabled()
  })

  it('submits with Enter, shows the loading state, then the answer with sources', async () => {
    const request = deferred()
    api.askQuestion.mockReturnValue(request.promise)
    render(<App />)

    fireEvent.change(questionBox(), { target: { value: 'What is the difference between List and Tuple?' } })
    fireEvent.keyDown(questionBox(), { key: 'Enter' })

    expect(api.askQuestion).toHaveBeenCalledWith('What is the difference between List and Tuple?')
    expect(screen.getByLabelText('Assistant is thinking')).toBeInTheDocument()
    expect(screen.getByText('In Progress')).toBeInTheDocument()
    expect(questionBox()).toHaveValue('')
    expect(sendButton()).toBeDisabled()

    await act(async () => request.resolve(relevantResponse))

    expect(screen.queryByLabelText('Assistant is thinking')).not.toBeInTheDocument()
    const answer = screen.getByText(/is mutable, a/).closest('.bubble')
    expect(within(answer).getByText('point = (10, 20)')).toBeInTheDocument()
    expect(within(answer).getByText('No correction needed')).toBeInTheDocument()
    expect(screen.getByText('Initial retrieval was relevant. No correction was required.')).toBeInTheDocument()

    fireEvent.click(within(answer).getByRole('button', { name: /Sources \(1\)/ }))
    expect(within(answer).getByText('Page 6')).toBeInTheDocument()
    expect(within(answer).getByText(/A tuple is an ordered collection/)).toBeInTheDocument()
  })

  it('submits a sample question when its card is clicked', async () => {
    api.askQuestion.mockResolvedValue(relevantResponse)
    render(<App />)

    fireEvent.click(screen.getByRole('button', { name: /What is Python\?/ }))

    expect(api.askQuestion).toHaveBeenCalledWith('What is Python?')
    await screen.findByText('No correction needed')
  })

  it('shows the corrective retrieval stage when a correction was used', async () => {
    api.askQuestion.mockResolvedValue(correctedResponse)
    render(<App />)

    fireEvent.click(screen.getByRole('button', { name: /OOPS/ }))

    expect(await screen.findByText('Corrective retrieval: 1 attempt')).toBeInTheDocument()
    const correctionStage = screen.getByText('Corrective Retrieval').closest('li')
    expect(correctionStage).toHaveClass('stage-corrected')
    expect(screen.getByText('Why rewritten: Expanded the abbreviation OOPS.')).toBeInTheDocument()
  })

  it('shows the safe message and no sources when the answer is not in the materials', async () => {
    api.askQuestion.mockResolvedValue(insufficientResponse)
    render(<App />)

    fireEvent.change(questionBox(), { target: { value: 'Who won the FIFA World Cup in 2022?' } })
    fireEvent.click(sendButton())

    expect(await screen.findByText(/could not find sufficient information/)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Sources/ })).not.toBeInTheDocument()
    expect(screen.getByText('Corrective retrieval: 2 attempts')).toBeInTheDocument()
  })

  it('shows a friendly error and lets the student retry', async () => {
    api.askQuestion.mockRejectedValueOnce(new Error('Network Error')).mockResolvedValueOnce(relevantResponse)
    render(<App />)

    fireEvent.change(questionBox(), { target: { value: 'What is a tuple?' } })
    fireEvent.click(sendButton())

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Cannot connect to the learning assistant server')
    fireEvent.click(within(alert).getByRole('button', { name: /Try again/ }))

    await screen.findByText('No correction needed')
    expect(api.askQuestion).toHaveBeenCalledTimes(2)
  })

  it('shows the error message sent by the backend', async () => {
    api.askQuestion.mockRejectedValue({ response: { status: 429, data: { detail: 'The AI service is busy.' } } })
    render(<App />)

    fireEvent.change(questionBox(), { target: { value: 'What is a tuple?' } })
    fireEvent.click(sendButton())

    expect(await screen.findByRole('alert')).toHaveTextContent('The AI service is busy.')
  })

  it('clears the conversation', async () => {
    api.askQuestion.mockResolvedValue(relevantResponse)
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /What is Python\?/ }))
    await screen.findByText('No correction needed')

    fireEvent.click(screen.getByRole('button', { name: /Clear chat/ }))

    await waitFor(() => expect(screen.getByText('Welcome to VPro Skills AI Learning Assistant')).toBeInTheDocument())
  })
})
