const Child = (props)=>{
    return(
        <>
            <p>{props.key1}</p>
            <p>{props.key2}</p>
            {
                !props.key3 ? <p>{props.key1}</p> : <p>{props.key2}</p>
            }
            {
                props.key4.map((element,index)=>{
                    return(<p key={index}>{element}</p>)
                })
            }
        </>
    )
}
export default Child