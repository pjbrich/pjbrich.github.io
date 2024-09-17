import logo from './exlterra.png';
import './App.css';
import React from 'react';
import MyButton from './MyButton'




function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>Scripts Here</h1>
      <MyButton />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://www.exlterra.com/"
          target="_blank"
          rel="noopener noreferrer"
          
        >
          Come check out our main website!
        </a>
      </header>
      
    </div>
  );
}

export default App;
