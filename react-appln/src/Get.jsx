import { useEffect, useState } from "react"
import axios from "axios"
const Get = ()=>{
    const [x,setX] = useState({})
    //make api calls
    useEffect(()=>{
        axios.get("https://jsonplaceholder.typicode.com/users").then((res)=>{
            setX(res)
        }).catch((err)=>{
            console.log(err)
        })
    },[])

    return(
        <>
            <p>{JSON.stringify(x)}</p>
        </>
    )
}
export default Get