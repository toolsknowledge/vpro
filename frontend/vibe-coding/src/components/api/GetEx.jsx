import { useEffect, useState } from 'react'
import axios from 'axios'

const URL = 'https://jsonplaceholder.typicode.com/posts'

function GetEx() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const getPosts = async () => {
      try {
        // GET -> read data from the server
        const res = await axios.get(URL, { params: { _limit: 5 } })
        setPosts(res.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    getPosts()
  }, [])

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}</p>

  return (
    <div>
      <h2>GET Example</h2>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  )
}

export default GetEx
