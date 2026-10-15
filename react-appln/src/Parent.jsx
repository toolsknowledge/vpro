import Child from "./Child"
import { useState } from "react";
const Parent = ()=>{
    const [msg,setMsg] = useState("VPro")
    return(
        <Child key1={msg}></Child>
    )
}
export default Parent