import { useRef } from "react";

function UseRefEx() {
  const inputRef = useRef(null);

  function focusInput() {
    inputRef.current.focus();
    console.log(inputRef.current.value)
  }

  return (
    <div>
      <input ref={inputRef} placeholder="Enter name" type="text"/>
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}

export default UseRefEx;