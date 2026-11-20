import { useState } from 'react';
import './Demo.css';

const features = [
  { icon: '⚡', title: 'Fast', text: 'Powered by Vite for instant dev server startup.' },
  { icon: '🧩', title: 'Reusable', text: 'Build UI from small, composable components.' },
  { icon: '🎨', title: 'Styled', text: 'Clean, responsive layout with plain CSS.' },
];

export default function Demo({ title = 'Welcome to Vibe App' }) {
  const [count, setCount] = useState(0);

  return (
    <section className="demo">
      <header className="demo__header">
        <h1>{title}</h1>
        <p>A basic presentation component built with React.</p>
      </header>

      <div className="demo__cards">
        {features.map((f) => (
          <article key={f.title} className="demo__card">
            <span className="demo__icon">{f.icon}</span>
            <h3>{f.title}</h3>
            <p>{f.text}</p>
          </article>
        ))}
      </div>

      <div className="demo__counter">
        <button onClick={() => setCount((c) => c - 1)}>−</button>
        <span>{count}</span>
        <button onClick={() => setCount((c) => c + 1)}>+</button>
      </div>
    </section>
  );
}
