import {BrowserRouter, Link, Route, Routes} from "react-router-dom"
import Laptops from "./Laptops.jsx"
import Mobiels from "./Mobiels.jsx"
const Electronics = ()=>{
    return(
        <>
            <BrowserRouter>
                <Link to={"/laptops"} style={{marginRight:100}}>
                        Laptops
                </Link>
                <Link to={"/mobiles"} style={{marginRight:100}}>
                    Mobiles
                </Link>
                <Routes>
                    <Route path="/laptops" element={<Laptops></Laptops>}></Route>
                    <Route path="/mobiles" element={<Mobiels></Mobiels>}></Route>
                </Routes>
            
            </BrowserRouter>
        </>
    )
}
export default Electronics