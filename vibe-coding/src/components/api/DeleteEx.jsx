import { useState } from 'react'
import axios from 'axios'

const URL = 'https://jsonplaceholder.typicode.com/posts'

function DeleteEx() {
  const [id, setId] = useState(1)
  const [message, setMessage] = useState('')

  const deletePost = async () => {
    try {
      // DELETE -> remove data from the server
      const res = await axios.delete(`${URL}/${id}`)
      setMessage(`Post ${id} deleted (status ${res.status})`)
    } catch (err) {
      setMessage(`Error: ${err.message}`)
    }
  }

  return (
    <div>
      <h2>DELETE Example</h2>
      <input type="number" value={id} onChange={(e) => setId(e.target.value)} placeholder="Post id" />
      <button onClick={deletePost}>Delete</button>
      {message && <p>{message}</p>}
    </div>
  )
}

export default DeleteEx
