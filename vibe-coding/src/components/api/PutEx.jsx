import { useState } from 'react'
import axios from 'axios'

const URL = 'https://jsonplaceholder.typicode.com/posts'

function PutEx() {
  const [id, setId] = useState(1)
  const [title, setTitle] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const updatePost = async () => {
    try {
      // PUT -> replace existing data on the server
      const res = await axios.put(`${URL}/${id}`, { id, title, body: 'Updated body', userId: 1 })
      setResult(res.data)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h2>PUT Example</h2>
      <input type="number" value={id} onChange={(e) => setId(e.target.value)} placeholder="Post id" />
      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="New title" />
      <button onClick={updatePost}>Update</button>
      {result && <p>Updated post id {result.id}: {result.title}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  )
}

export default PutEx
