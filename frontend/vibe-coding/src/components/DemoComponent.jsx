import './DemoComponent.css'

function DemoComponent() {
  return (
    <div className="demo-container">
      <h1>Demo Component</h1>
      <p>This is a sample React component with static dummy data.</p>

      <h2>Employee List</h2>
      <table className="demo-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Role</th>
            <th>City</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>101</td>
            <td>Ravi Kumar</td>
            <td>Frontend Developer</td>
            <td>Hyderabad</td>
          </tr>
          <tr>
            <td>102</td>
            <td>Priya Sharma</td>
            <td>Backend Developer</td>
            <td>Bangalore</td>
          </tr>
          <tr>
            <td>103</td>
            <td>Arjun Reddy</td>
            <td>UI/UX Designer</td>
            <td>Chennai</td>
          </tr>
          <tr>
            <td>104</td>
            <td>Sneha Patel</td>
            <td>QA Engineer</td>
            <td>Pune</td>
          </tr>
        </tbody>
      </table>

      <h2>Technologies</h2>
      <ul className="demo-list">
        <li>HTML</li>
        <li>CSS</li>
        <li>JavaScript</li>
        <li>React</li>
      </ul>
    </div>
  )
}

export default DemoComponent
