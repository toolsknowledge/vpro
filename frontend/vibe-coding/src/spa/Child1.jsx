import { Link, Outlet } from "react-router-dom"

const Child1 = () => {
    return (
        <>
            <h2>Child1 Component</h2>
            <nav>
                <Link to="subchild1" style={{ marginRight: 20 }}>Subchild1</Link>
                <Link to="subchild2">Subchild2</Link>
            </nav>
            <Outlet />
        </>
    )
}
export default Child1
