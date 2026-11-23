import { useState } from "react";

const State = ()=>{
    const [name,setName] = useState("VPro")
    const [num1,setNum1] = useState(200)
    const [num2,setNum2] = useState(100)
    const [flag,setFlag] = useState(true)
    const [arr,setArr] = useState([10,20,30,40,50])
    const test_func1 = ()=>{
        setNum1(num1 + 1)
    }
    const test_func2 = ()=>{
        setNum2(num2 - 1)
    }
    return(
        <>
            <button onClick={test_func1}>
                ClickMe
            </button>

            <button onClick={test_func2}>
                ClickMe1
            </button>
            
            
            {
                arr.map((element,index)=>{
                    return(<p key={index}>{element}</p>)
                })
            }
            
            
            <p>{name}</p>
            <p>Addition. {num1+num2}</p>
            <p>Subtraction. {num1-num2}</p>
            {
                flag ? <p>{num1}</p> : <p>{num2}</p>
            }
            {
                !flag ? <p>{num1}</p> : <p>{num2}</p>
            }
        </>
    )
}
export default State