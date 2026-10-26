import MyContext from './MyContext'
import Demo2 from './Demo2'

function Demo1() {
  const data = {
    name: 'Ravi Kumar', // string
    id: 101, // number (int)
    salary: 45000.75, // number (float)
    isActive: true, // boolean
    skills: ['HTML', 'CSS', 'React'], // array
    address: { city: 'Hyderabad', pin: 500001 }, // object
    projects: [
      { pid: 1, title: 'E-Commerce App' },
      { pid: 2, title: 'Chat App' },
    ], // array of objects
    manager: null, // null
    bonus: undefined, // undefined
    greet: (msg) => alert(`Demo1 received: ${msg}`), // function
  }

  return (
    <MyContext.Provider value={data}>
      <h2>Demo1 (Provider)</h2>
      <Demo2 />
    </MyContext.Provider>
  )
}

export default Demo1
