import { useState } from "react";

function useVPro() {
  const [count, setCount] = useState(0);

  function increase() {
    setCount((previous) => previous + 1);
  }

  return { count, increase };
}

export default useVPro;

/**
 * useVPro() - custom hook
 * 
 */

/**
 * useState()
 * useEffect()
 * useRef()
 * ---
 * ---
 */