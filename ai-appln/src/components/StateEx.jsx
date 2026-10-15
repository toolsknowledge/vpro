import { useState } from "react";

function StateEx() {
  // String
  const [name, setName] = useState("Samba");

  // Number
  const [count, setCount] = useState(0);

  // Boolean
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Array
  const [fruits, setFruits] = useState(["Apple", "Banana"]);

  // Object
  const [user, setUser] = useState({ city: "Hyderabad", age: 25 });

  return (
    <div>
      <h2>useState() Example</h2>

      <h3>1. String</h3>
      <p>Name: {name}</p>
      <button onClick={() => setName("React")}>Change Name</button>

      <h3>2. Number</h3>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)}>Decrement</button>

      <h3>3. Boolean</h3>
      <p>Status: {isLoggedIn ? "Logged In" : "Logged Out"}</p>
      <button onClick={() => setIsLoggedIn(!isLoggedIn)}>Toggle</button>

      <h3>4. Array</h3>
      <ul>
        {fruits.map((fruit, index) => (
          <li key={index}>{fruit}</li>
        ))}
      </ul>
      <button onClick={() => setFruits([...fruits, "Mango"])}>Add Fruit</button>

      <h3>5. Object</h3>
      <p>City: {user.city}, Age: {user.age}</p>
      <button onClick={() => setUser({ ...user, age: user.age + 1 })}>
        Increase Age
      </button>
    </div>
  );
}

export default StateEx;
