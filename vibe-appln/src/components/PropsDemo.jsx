import { useState } from 'react';
import './PropsDemo.css';

// Child: receives data via props (read-only), including a function prop and children
function UserCard({ name, age, skills, address, isActive, onGreet, children, role = 'Guest' }) {
  return (
    <div className={`pd__card ${isActive ? 'pd__card--active' : ''}`}>
      <h3>{name} <small>({role})</small></h3>
      <p>Age: {age}</p>
      <p>Status: {isActive ? 'Active' : 'Inactive'}</p>
      <p>City: {address.city}, {address.country}</p>
      <p>Skills: {skills.join(', ')}</p>
      <button onClick={() => onGreet(name)}>Greet</button>
      <div className="pd__children">{children}</div>
    </div>
  );
}

// Parent: owns state and passes it down as props
export default function PropsDemo() {
  const [message, setMessage] = useState('Click a Greet button');
  const [age, setAge] = useState(25);

  const users = [
    { id: 1, name: 'Sam', skills: ['React', 'JS'], address: { city: 'Hyderabad', country: 'India' }, isActive: true, role: 'Admin' },
    { id: 2, name: 'Ravi', skills: ['Python'], address: { city: 'Pune', country: 'India' }, isActive: false },
  ];

  return (
    <section className="pd">
      <h2>Props demo</h2>
      <p className="pd__msg">{message}</p>
      <button onClick={() => setAge((a) => a + 1)}>Increase Sam's age (state → prop)</button>

      {users.map((u, i) => (
        <UserCard
          key={u.id}
          name={u.name}
          age={i === 0 ? age : 30}
          skills={u.skills}
          address={u.address}
          isActive={u.isActive}
          role={u.role}
          onGreet={(n) => setMessage(`Hello from ${n}!`)}
        >
          <em>Child content passed via children prop</em>
        </UserCard>
      ))}
    </section>
  );
}
