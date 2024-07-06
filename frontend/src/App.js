import logo from './logo.svg';
import axios from 'axios';
import React, { useState} from 'react';
import './App.css';

function App() {
  const [alive, setStatus] = useState(null);

  const pingServer = async () => {
    const response = await axios.get('http://127.0.0.1:8000');
    setStatus(response.data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <button className="ping-check-button" onClick={pingServer}>
        ping server
        </button>
        {alive && (
          <div className={`ping-status ${alive === 'ping' ? 'ping' : 'error'}`}>
            response from api: {alive}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
