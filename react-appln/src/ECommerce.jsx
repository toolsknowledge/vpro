//import all child components
import Laptops from "./Laptops"
import Mobiles from "./Mobiles"
import Watches from "./Watches"
import Dell from "./Dell"
import Hp from "./Hp"

/**
 * Link - create the router links (hyperlinks)
 * Route - create routings (navigations)
 * Routes - encapsulate the routings (packing of routing)
 * BrowserRouter - used to handle the dynamic routings
 * Link, Route, Routes and BrowserRouter are the predefined components
 */
import {Link,Route,Routes,BrowserRouter} from "react-router-dom"
const ECommerce = ()=>{
    return(
        <>
            <BrowserRouter>
                <Link to="/laptops" style={{marginRight:200}}>
                    Laptops
                </Link>
                <Link to="/mobiles" style={{marginRight:200}}>
                    Mobiles
                </Link>
                <Link to="/watches">
                    Watches
                </Link>
                <Routes>
                    <Route path="/laptops" element={<Laptops></Laptops>}>
                        <Route path="laptops/dell" element={<Dell></Dell>}></Route>
                        <Route path="laptops/hp" element={<Hp></Hp>}></Route>
                    </Route>


                    <Route path="/mobiles" element={<Mobiles></Mobiles>}>

                    </Route>

                    <Route path="/watches" element={<Watches></Watches>}>
                        
                    </Route>
                </Routes>
            </BrowserRouter>

        </>
    )
}
export default ECommerce