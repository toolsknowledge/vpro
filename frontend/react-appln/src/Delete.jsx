import axios from "axios"
import { useState } from "react"
const Delete = ()=>{
    const [x,setX] = useState({})
    const demo_func = ()=>{
        axios.delete("https://jsonplaceholder.typicode.com/users/1").then((res)=>{
            setX(res)
        }).catch((err)=>{
            console.log(err)
        })
    }
    
    return(
        <>
        <button onClick={demo_func}>
            Click Me
        </button>
        <p>{JSON.stringify(x)}</p>
        </>
    )
}
export default Delete