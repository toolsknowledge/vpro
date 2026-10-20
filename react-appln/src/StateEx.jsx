import { useState } from "react";

const StateEx = ()=>{
    const [msg,setMsg] = useState("Hello,React")
    const [num1,setNum1] = useState(0)
    return(
        <>
            <h1>{msg}</h1>
            <h1>{num1}</h1>
            <button onClick={()=>setNum1(num1+1)}>Increment</button>
            <button onClick={()=>setNum1(num1-1)}>Decrement</button>
        </>
    )
}
export default StateEx;