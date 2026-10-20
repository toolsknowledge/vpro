import Child from './Child'
import './PropsEx.css'

function Parent() {
  // data owned by the Parent component
  const id = 101 // number
  const name = 'Ravi Kumar' // string
  const isActive = true // boolean
  const skills = ['HTML', 'CSS', 'JavaScript', 'React'] // array
  const address = { city: 'Hyderabad', state: 'Telangana', pin: 500001 } // object
  const projects = [
    { pid: 1, title: 'E-Commerce App', duration: '3 months' },
    { pid: 2, title: 'Chat Application', duration: '2 months' },
  ] // array of objects
  const manager = null // null
  const bonus = undefined // undefined

  // function
  const greet = (msg) => {
    alert(`Parent received: ${msg}`)
  }

  return (
    <div className="props-container">
      <h1>Props in React</h1>
      <p>
        The Parent component passes data to the Child component with the help of
        props. Props are immutable — the Child can read them but cannot change them.
      </p>

      <div className="parent-box">
        <h2>Parent Component</h2>
        <Child
          id={id}
          name={name}
          isActive={isActive}
          skills={skills}
          address={address}
          projects={projects}
          manager={manager}
          bonus={bonus}
          greet={greet}
        />
      </div>
    </div>
  )
}

export default Parent
