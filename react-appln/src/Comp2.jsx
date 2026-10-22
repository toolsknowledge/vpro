import { useContext } from "react"
import { MyContext } from "./MyContext"
const Comp2 = ()=>{
    const res = useContext(MyContext)
    return(
        <h1>{res}</h1>
    )
}
export default Comp2