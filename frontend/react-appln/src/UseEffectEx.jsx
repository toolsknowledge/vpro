import { useEffect } from "react";

function UseEffectEx() {
  useEffect(() => {
    console.log("Component loaded / HTML Loaded Successfully !!!");
  }, []);

  return <h2>Hello React</h2>;
}

export default UseEffectEx;