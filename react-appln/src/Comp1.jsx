/**
 * useState() - hook
 * ready made - define the variables Ex. x,y,num1,num2,....
 * 
 */
import { useState } from "react"

const Comp1 = ()=>{
    const [x,setX] = useState(200)
    const [y,setY] = useState(100)
    const [flag,setFlag] = useState(true)
    const [menu,setMenu] = useState(["Courses","Batches","Syllabus","Login","Logout"])
    return(
        <>
            <p>Addition. {x+y}</p>
            <hr></hr>

            {
                flag ? <p style={{color:"red"}}>{x}</p> : <p>{y}</p>
            }

            {
                menu.map((element,index)=>{
                    return(<p>{element}</p>)
                })
            }
        </>
    )
}
export default Comp1