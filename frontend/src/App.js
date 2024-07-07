import axios from "axios";
import React, { useState } from "react";
import "./App.css";

function App() {
  const [alive, setStatus] = useState(null);
  // define a state to store the categories with an empty array
  const [categories, getCategories] = useState([]);
  const pingServer = async () => {
    const response = await axios.get("http://127.0.0.1:8000");
    setStatus(response.data);
  };

  const fetchCategory = async () => {
    const cat_response = await axios.get("http://127.0.0.1:8000/categories/");
    console.log(cat_response.data);
    getCategories(cat_response.data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <button className="test-btn" onClick={pingServer}>
          ping server
        </button>
        {alive && (
          <div className={`ping-status`}>
            response from API: {alive}
          </div>
        )}
        <button className="test-btn" onClick={fetchCategory}>
          fetch category
        </button>
        {categories.length > 0 && (
            <div className={`ping-status`}>
                response from API:{" "}
                <ul>
                  {categories.map((category) => (
                    <li key={category.id}>{category.name}</li>
                  ))}
                </ul>
            </div>
          )}
      </header>
    </div>
  );
}

export default App;
