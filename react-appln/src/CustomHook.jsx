import useVPro from "./useVPro";

function CustomHook() {
  const { count, increase } = useVPro();

  return (
    <div>
      <h2>Count: {count}</h2>
      <button onClick={increase}>
        Increase
      </button>
    </div>
  );
}

export default CustomHook;