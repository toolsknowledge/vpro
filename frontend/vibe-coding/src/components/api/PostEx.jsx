import { useState } from 'react'
import axios from 'axios'

const URL = 'https://jsonplaceholder.typicode.com/posts'

function PostEx() {
  const [title, setTitle] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const createPost = async () => {
    try {
      // POST -> create new data on the server
      const res = await axios.post(URL, { title, body: 'Sample body', userId: 1 })
      setResult(res.data)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h2>POST Example</h2>
      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Enter title" />
      <button onClick={createPost}>Create</button>
      {result && <p>Created post id {result.id}: {result.title}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  )
}

export default PostEx
