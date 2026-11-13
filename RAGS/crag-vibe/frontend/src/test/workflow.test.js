import { describe, expect, it } from 'vitest'
import { buildWorkflowStages } from '../workflow'
import { correctedResponse, insufficientResponse, relevantResponse } from './fixtures'

const statuses = (response) => buildWorkflowStages(response).map((stage) => stage.status)

describe('buildWorkflowStages', () => {
  it('marks correction as not needed when the first retrieval was relevant', () => {
    const stages = buildWorkflowStages(relevantResponse)

    expect(stages).toHaveLength(6)
    expect(statuses(relevantResponse)).toEqual(['completed', 'completed', 'completed', 'completed', 'skipped', 'completed'])
    expect(stages[4].details).toEqual(['Initial retrieval was relevant. No correction was required.'])
  })

  it('highlights a successful correction', () => {
    expect(statuses(correctedResponse)).toEqual(['completed', 'completed', 'completed', 'failed', 'corrected', 'completed'])
    expect(buildWorkflowStages(correctedResponse)[4].details[0]).toContain('object-oriented programming classes objects')
  })

  it('marks correction and answer as failed when nothing relevant was found', () => {
    expect(statuses(insufficientResponse)).toEqual(['completed', 'completed', 'completed', 'failed', 'failed', 'failed'])
  })
})
