import { useMemo, useState } from "react";

function UseMemoEx() {
  const [number, setNumber] = useState(2);

  const square = useMemo(() => {
    console.log("Calculating square");
    return number * number;
  }, [number]);

  return (
    <div>
      <h2>Square: {square}</h2>
      <button onClick={() => setNumber(number + 1)}>
        Change Number
      </button>
    </div>
  );
}

export default UseMemoEx;