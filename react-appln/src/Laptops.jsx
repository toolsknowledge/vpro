import { Link,Outlet } from "react-router-dom"
const Laptops = ()=>{
    return(
        <>
            <p>Laptops Soon...!</p>
            <Link to="laptops/dell" style={{marginRight:200}}>Dell</Link>
            <Link to="laptops/hp">Hp</Link>
            <br></br><br></br>
            <Outlet></Outlet>
        </>
    )
}
export default Laptops