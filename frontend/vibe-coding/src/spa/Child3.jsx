import { Link, Outlet } from "react-router-dom"

const Child3 = () => {
    return (
        <>
            <h2>Child3 Component</h2>
            <nav>
                <Link to="subchild5" style={{ marginRight: 20 }}>Subchild5</Link>
                <Link to="subchild6">Subchild6</Link>
            </nav>
            <Outlet />
        </>
    )
}
export default Child3
