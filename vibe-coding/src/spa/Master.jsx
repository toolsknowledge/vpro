import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router-dom"
import Child1 from "./Child1.jsx"
import Child2 from "./Child2.jsx"
import Child3 from "./Child3.jsx"
import Subchild1 from "./Subchild1.jsx"
import Subchild2 from "./Subchild2.jsx"
import Subchild3 from "./Subchild3.jsx"
import Subchild4 from "./Subchild4.jsx"
import Subchild5 from "./Subchild5.jsx"
import Subchild6 from "./Subchild6.jsx"

const Master = () => {
    return (
        <BrowserRouter>
            <h1>Master</h1>
            <nav>
                <Link to="/child1" style={{ marginRight: 20 }}>Child1</Link>
                <Link to="/child2" style={{ marginRight: 20 }}>Child2</Link>
                <Link to="/child3">Child3</Link>
            </nav>
            <Routes>
                <Route path="/" element={<Navigate to="/child1" />} />
                <Route path="/child1" element={<Child1 />}>
                    <Route path="subchild1" element={<Subchild1 />} />
                    <Route path="subchild2" element={<Subchild2 />} />
                </Route>
                <Route path="/child2" element={<Child2 />}>
                    <Route path="subchild3" element={<Subchild3 />} />
                    <Route path="subchild4" element={<Subchild4 />} />
                </Route>
                <Route path="/child3" element={<Child3 />}>
                    <Route path="subchild5" element={<Subchild5 />} />
                    <Route path="subchild6" element={<Subchild6 />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}
export default Master
