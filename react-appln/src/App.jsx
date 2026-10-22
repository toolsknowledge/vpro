import { MyContext } from "./MyContext"
import Comp1 from "./Comp1"
import Comp2 from "./Comp2"
const App = ()=>{
  return(
    <MyContext.Provider value={"Hello,Vpro !!!"}>
        <Comp1></Comp1>
        <Comp2></Comp2>
    </MyContext.Provider>
  )
}
export default App