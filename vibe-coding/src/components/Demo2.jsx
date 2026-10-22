import { useContext } from 'react'
import MyContext from './MyContext'

function Demo2() {
  const { name, id, salary, isActive, skills, address, projects, manager, bonus, greet } =
    useContext(MyContext)

  return (
    <div>
      <h2>Demo2 (Consumer)</h2>
      <p>String: {name}</p>
      <p>Int: {id}</p>
      <p>Float: {salary}</p>
      <p>Boolean: {isActive ? 'true' : 'false'}</p>
      <p>Array: {skills.join(', ')}</p>
      <p>Object: {address.city} - {address.pin}</p>
      <ul>
        Array of Objects:
        {projects.map((p) => (
          <li key={p.pid}>{p.title}</li>
        ))}
      </ul>
      <p>Null: {manager === null ? 'null' : manager}</p>
      <p>Undefined: {bonus === undefined ? 'undefined' : bonus}</p>
      <button onClick={() => greet('Hello from Demo2')}>Function</button>
    </div>
  )
}

export default Demo2
