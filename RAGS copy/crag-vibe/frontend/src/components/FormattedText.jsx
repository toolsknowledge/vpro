/**
 * Renders the small Markdown subset the assistant uses: paragraphs, headings, bullet and numbered
 * lists, **bold**, `inline code` and ``` code blocks. React escapes all text, so this is XSS-safe.
 */

function renderInline(text) {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, index) => {
    if (part.length > 4 && part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index}>{part.slice(2, -2)}</strong>
    }
    if (part.length > 2 && part.startsWith('`') && part.endsWith('`')) {
      return <code key={index}>{part.slice(1, -1)}</code>
    }
    return part
  })
}

export default function FormattedText({ text }) {
  const blocks = []
  let paragraph = []
  let list = null

  const flushParagraph = () => {
    if (paragraph.length) {
      blocks.push(<p key={blocks.length}>{renderInline(paragraph.join(' '))}</p>)
      paragraph = []
    }
  }
  const flushList = () => {
    if (list) {
      const ListTag = list.type
      blocks.push(
        <ListTag key={blocks.length}>
          {list.items.map((item, index) => (
            <li key={index} className={item.nested ? 'nested' : undefined}>{renderInline(item.text)}</li>
          ))}
        </ListTag>,
      )
      list = null
    }
  }

  text.split('```').forEach((segment, segmentIndex) => {
    if (segmentIndex % 2 === 1) {
      flushParagraph()
      flushList()
      const code = segment.replace(/^[\w+-]*\n/, '').replace(/\n+$/, '')
      blocks.push(<pre key={blocks.length}><code>{code}</code></pre>)
      return
    }
    for (const line of segment.split('\n')) {
      const heading = line.match(/^#{1,6}\s+(.*)$/)
      const item = line.match(/^(\s*)(?:[-*•]|(\d+)[.)])\s+(.*)$/)
      if (!line.trim()) {
        flushParagraph()
        flushList()
      } else if (heading) {
        flushParagraph()
        flushList()
        blocks.push(<h4 key={blocks.length}>{renderInline(heading[1])}</h4>)
      } else if (item) {
        flushParagraph()
        const type = item[2] ? 'ol' : 'ul'
        const nested = item[1].length > 0
        if (!list || (list.type !== type && !nested)) {
          flushList()
          list = { type, items: [] }
        }
        list.items.push({ text: item[3], nested })
      } else if (list && /^\s+/.test(line)) {
        list.items[list.items.length - 1].text += ` ${line.trim()}`
      } else {
        flushList()
        paragraph.push(line.trim())
      }
    }
  })
  flushParagraph()
  flushList()

  return <div className="formatted-text">{blocks}</div>
}
