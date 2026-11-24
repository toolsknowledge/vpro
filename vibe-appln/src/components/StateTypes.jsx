import { useState } from 'react';
import './StateTypes.css';

export default function StateTypes() {
  // Number
  const [count, setCount] = useState(0);
  // String
  const [name, setName] = useState('React');
  // Boolean
  const [isOn, setIsOn] = useState(false);
  // Array
  const [items, setItems] = useState(['apple', 'banana']);
  const [newItem, setNewItem] = useState('');
  // Object
  const [user, setUser] = useState({ name: 'Sam', age: 25 });
  // null (empty until chosen)
  const [selected, setSelected] = useState(null);
  // undefined (no initial value)
  const [maybe, setMaybe] = useState();
  // BigInt
  const [big, setBig] = useState(9007199254740991n);
  // Symbol
  const [sym, setSym] = useState(Symbol('id'));

  const addItem = () => {
    if (!newItem.trim()) return;
    setItems((prev) => [...prev, newItem.trim()]);
    setNewItem('');
  };

  return (
    <section className="st">
      <h2>useState with all data types</h2>

      <div className="st__box">
        <h3>Number</h3>
        <p>{count}</p>
        <button onClick={() => setCount((c) => c - 1)}>-</button>
        <button onClick={() => setCount((c) => c + 1)}>+</button>
        <button onClick={() => setCount(0)}>Reset</button>
      </div>

      <div className="st__box">
        <h3>String</h3>
        <input value={name} onChange={(e) => setName(e.target.value)} />
        <p>Hello, {name || 'stranger'}!</p>
      </div>

      <div className="st__box">
        <h3>Boolean</h3>
        <p>The switch is {isOn ? 'ON' : 'OFF'}</p>
        <button onClick={() => setIsOn((v) => !v)}>Toggle</button>
      </div>

      <div className="st__box">
        <h3>Array</h3>
        <ul>
          {items.map((item, i) => (
            <li key={i}>
              {item}{' '}
              <button onClick={() => setItems(items.filter((_, idx) => idx !== i))}>x</button>
            </li>
          ))}
        </ul>
        <input value={newItem} onChange={(e) => setNewItem(e.target.value)} placeholder="New item" />
        <button onClick={addItem}>Add</button>
      </div>

      <div className="st__box">
        <h3>Object</h3>
        <p>{user.name}, age {user.age}</p>
        <input value={user.name} onChange={(e) => setUser({ ...user, name: e.target.value })} />
        <button onClick={() => setUser((u) => ({ ...u, age: u.age + 1 }))}>Birthday</button>
      </div>

      <div className="st__box">
        <h3>null</h3>
        <p>Selected: {selected === null ? 'null (nothing)' : selected}</p>
        <button onClick={() => setSelected('Option A')}>Select A</button>
        <button onClick={() => setSelected(null)}>Clear</button>
      </div>

      <div className="st__box">
        <h3>undefined</h3>
        <p>Value: {maybe === undefined ? 'undefined' : maybe}</p>
        <button onClick={() => setMaybe('defined now')}>Define</button>
        <button onClick={() => setMaybe(undefined)}>Undefine</button>
      </div>

      <div className="st__box">
        <h3>BigInt</h3>
        <p>{big.toString()}</p>
        <button onClick={() => setBig((b) => b + 1n)}>+1n</button>
      </div>

      <div className="st__box">
        <h3>Symbol</h3>
        <p>{sym.toString()}</p>
        <button onClick={() => setSym(Symbol('id'))}>New Symbol</button>
      </div>
    </section>
  );
}
