import { Link, Outlet } from "react-router-dom"

const Child2 = () => {
    return (
        <>
            <h2>Child2 Component</h2>
            <nav>
                <Link to="subchild3" style={{ marginRight: 20 }}>Subchild3</Link>
                <Link to="subchild4">Subchild4</Link>
            </nav>
            <Outlet />
        </>
    )
}
export default Child2
