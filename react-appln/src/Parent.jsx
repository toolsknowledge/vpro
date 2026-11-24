import Child from "./Child.jsx"
const Parent = ()=>{
    return(
        <>
            <Child key1={"Hello"} 
                   key2={100}
                   key3={true}
                   key4={["Python","ML","DL","NLP","GENAI","AGENTICAI"]}></Child>
        </>
    )
}
export default Parent