import { useState } from 'react'
import './StateEx.css'

function StateEx() {
  // 1) number
  const [count, setCount] = useState(0)

  // 2) string
  const [name, setName] = useState('Ravi')

  // 3) boolean
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  // 4) array
  const [skills, setSkills] = useState(['HTML', 'CSS', 'JavaScript'])

  // 5) object
  const [user, setUser] = useState({ id: 101, name: 'Priya', city: 'Hyderabad' })

  // 6) array of objects
  const [products, setProducts] = useState([
    { id: 1, name: 'Laptop', price: 50000 },
    { id: 2, name: 'Mobile', price: 20000 },
  ])

  // 7) null
  const [message, setMessage] = useState(null)

  // 8) undefined
  const [result, setResult] = useState(undefined)

  return (
    <div className="state-container">
      <h1>State in React</h1>
      <p>
        State represents component data. State is mutable — when it changes, React
        re-renders the component.
      </p>

      <section>
        <h2>1) Number</h2>
        <p>Count: {count}</p>
        <button onClick={() => setCount(count + 1)}>Increment</button>
        <button onClick={() => setCount(count - 1)}>Decrement</button>
        <button onClick={() => setCount(0)}>Reset</button>
      </section>

      <section>
        <h2>2) String</h2>
        <p>Name: {name}</p>
        <input value={name} onChange={(e) => setName(e.target.value)} />
        <button onClick={() => setName('Arjun')}>Change to Arjun</button>
      </section>

      <section>
        <h2>3) Boolean</h2>
        <p>Status: {isLoggedIn ? 'Logged In' : 'Logged Out'}</p>
        <button onClick={() => setIsLoggedIn(!isLoggedIn)}>
          {isLoggedIn ? 'Logout' : 'Login'}
        </button>
      </section>

      <section>
        <h2>4) Array</h2>
        <ul>
          {skills.map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>
        <button onClick={() => setSkills([...skills, 'React'])}>Add React</button>
        <button onClick={() => setSkills(skills.slice(0, -1))}>Remove Last</button>
      </section>

      <section>
        <h2>5) Object</h2>
        <p>
          ID: {user.id} | Name: {user.name} | City: {user.city}
        </p>
        <button onClick={() => setUser({ ...user, city: 'Bangalore' })}>
          Change City to Bangalore
        </button>
        <button onClick={() => setUser({ ...user, name: 'Sneha' })}>
          Change Name to Sneha
        </button>
      </section>

      <section>
        <h2>6) Array of Objects</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.id}</td>
                <td>{product.name}</td>
                <td>₹{product.price}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button
          onClick={() =>
            setProducts([
              ...products,
              { id: products.length + 1, name: 'Tablet', price: 30000 },
            ])
          }
        >
          Add Product
        </button>
      </section>

      <section>
        <h2>7) Null</h2>
        <p>Message: {message === null ? 'null (no message yet)' : message}</p>
        <button onClick={() => setMessage('Welcome to React State!')}>Set Message</button>
        <button onClick={() => setMessage(null)}>Clear (null)</button>
      </section>

      <section>
        <h2>8) Undefined</h2>
        <p>Result: {result === undefined ? 'undefined (not calculated)' : result}</p>
        <button onClick={() => setResult(10 + 20)}>Calculate 10 + 20</button>
        <button onClick={() => setResult(undefined)}>Reset (undefined)</button>
      </section>
    </div>
  )
}

export default StateEx
