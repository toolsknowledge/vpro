import { createContext, useContext } from "react";

// context (or) gloabl
// no data (ContextEx) will store data (Provider)
const NameContext = createContext();

function Child() {
  const name = useContext(NameContext);

  return <h2>Hello {name}</h2>;
}

function ContextEx() {
  return (
    <NameContext.Provider value="Ravi">
      <Child />
    </NameContext.Provider>
  );
}

export default ContextEx;