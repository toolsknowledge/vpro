function Child(props) {
  const { id, name, isActive, skills, address, projects, manager, bonus, greet } = props

  return (
    <div className="child-box">
      <h2>Child Component</h2>

      <section>
        <h3>1) Number</h3>
        <p>ID: {id}</p>
      </section>

      <section>
        <h3>2) String</h3>
        <p>Name: {name}</p>
      </section>

      <section>
        <h3>3) Boolean</h3>
        <p>Status: {isActive ? 'Active' : 'Inactive'}</p>
      </section>

      <section>
        <h3>4) Array</h3>
        <ul>
          {skills.map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>5) Object</h3>
        <p>
          City: {address.city} | State: {address.state} | PIN: {address.pin}
        </p>
      </section>

      <section>
        <h3>6) Array of Objects</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            {projects.map((project) => (
              <tr key={project.pid}>
                <td>{project.pid}</td>
                <td>{project.title}</td>
                <td>{project.duration}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h3>7) Null</h3>
        <p>Manager: {manager === null ? 'null (not assigned)' : manager}</p>
      </section>

      <section>
        <h3>8) Undefined</h3>
        <p>Bonus: {bonus === undefined ? 'undefined (not decided)' : bonus}</p>
      </section>

      <section>
        <h3>9) Function</h3>
        <button onClick={() => greet('Hello from Child!')}>Call Parent Function</button>
      </section>
    </div>
  )
}

export default Child
