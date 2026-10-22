import axios from "axios"
import { useState } from "react"
const Put = ()=>{
    const [x,setX] = useState({})
    const demo_func = ()=>{
        axios.put("https://jsonplaceholder.typicode.com/users/1",{
            "name":"Samba P",
            "email":"samba.pendela@gmail.com"
        }).then((res)=>{
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
export default Put