import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import FormattedText from '../components/FormattedText'

describe('FormattedText', () => {
  it('renders bold text, lists, inline code and code blocks', () => {
    const { container } = render(
      <FormattedText text={'A **list** uses `[]`.\n\n- first\n- second\n\n```python\nx = [1, 2]\n```'} />,
    )

    expect(screen.getByText('list').tagName).toBe('STRONG')
    expect(screen.getByText('[]').tagName).toBe('CODE')
    expect(container.querySelectorAll('li')).toHaveLength(2)
    expect(container.querySelector('pre code')).toHaveTextContent('x = [1, 2]')
  })

  it('never renders HTML from the answer', () => {
    const { container } = render(<FormattedText text={'<img src=x onerror=alert(1)>'} />)

    expect(container.querySelector('img')).toBeNull()
  })
})
