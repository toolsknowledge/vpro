// Small inline SVG icons (no icon library needed).
const base = {
  width: 18,
  height: 18,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  'aria-hidden': true,
}

export const SendIcon = (props) => (
  <svg {...base} {...props}><path d="M22 2 11 13" /><path d="M22 2 15 22l-4-9-9-4 20-7Z" /></svg>
)
export const TrashIcon = (props) => (
  <svg {...base} {...props}><path d="M3 6h18" /><path d="M8 6V4h8v2" /><path d="M19 6l-1 14H6L5 6" /></svg>
)
export const ChevronIcon = (props) => (
  <svg {...base} {...props}><path d="m6 9 6 6 6-6" /></svg>
)
export const DocumentIcon = (props) => (
  <svg {...base} {...props}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><path d="M14 2v6h6" /><path d="M8 13h8M8 17h5" /></svg>
)
export const AlertIcon = (props) => (
  <svg {...base} {...props}><circle cx="12" cy="12" r="10" /><path d="M12 8v4M12 16h.01" /></svg>
)
export const RefreshIcon = (props) => (
  <svg {...base} {...props}><path d="M21 12a9 9 0 1 1-3-6.7L21 8" /><path d="M21 3v5h-5" /></svg>
)
export const SparkIcon = (props) => (
  <svg {...base} {...props}><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8" /></svg>
)
export const FlowIcon = (props) => (
  <svg {...base} {...props}><rect x="3" y="3" width="6" height="6" rx="1" /><rect x="15" y="15" width="6" height="6" rx="1" /><path d="M9 6h4a2 2 0 0 1 2 2v7" /></svg>
)
