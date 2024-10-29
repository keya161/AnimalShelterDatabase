// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [animals, setAnimals] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/animals")
      .then(response => {
        console.log(response.data); // Log the data to check its structure
        setAnimals(response.data);
      })
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h2>Animals List</h2>
      <ul>
        {animals.map((animal, index) => (
          <li key={index}>{animal.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
