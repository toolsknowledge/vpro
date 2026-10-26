import { useCallback, useState } from "react";

function UseCallbackEx() {
  const [count, setCount] = useState(0);

  const sayHello = useCallback(() => {
    console.log("Hello React");
  }, []);

  return (
    <div>
      <h2>{count}</h2>
      <button onClick={() => setCount(count + 1)}>
        Increase
      </button>
      <button onClick={sayHello}>
        Say Hello
      </button>
    </div>
  );
}

export default UseCallbackEx;