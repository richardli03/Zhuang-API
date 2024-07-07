import axios from "axios";
import React, { useState } from "react";
import "./App.css";

function SetInput(){
  const [exerciseName, setName] = useState('');
  const [sets, setSets] = useState([{ weight: '', reps: '' }]);
  const [workoutID, setWorkoutID] = useState(null);
  
  const handleNameChange = (event) => {
    setName(event.target.value);
  };
  
  const handleWorkoutID = (id) => {
    setWorkoutID(id.target.value);
  }
  const handleSetInput = (index, event) => {
    const { name, value } = event.target;
    const newSets = [...sets];
    newSets[index][name] = value;
    setSets(newSets);
  };

  const addSet = () => {
    setSets([...sets, { weight: '', reps: '' }]);
  };

  const removeSet = (index) => {
    const newSets = sets.filter((_, i) => i !== index);
    setSets(newSets);
  };

  const submitSets = async () => {
    try {
      const formattedSets = sets.map(set => ({
        weight: parseFloat(set.weight),
        reps: parseInt(set.reps, 10)
      })).filter(set => set.weight && set.reps); // Remove any incomplete sets
      
      const exerciseData = {
        workout_id: workoutID,
        name: exerciseName,
        set_info: formattedSets
      };

      console.log('Formatted sets:', exerciseData);
      const response = await axios.post('http://127.0.0.1:8000/entries/', exerciseData);
      console.log('Exercises logged:', response.data);
      // clearrrrrrr
      setName('');
      setSets([{ weight: '', reps: '' }]);
      // leaving workout id
      // setWorkoutID(null);
    } catch (error) {
      console.error('Error logging exercises:', error);
    }
  };

  return (
    <div>
      <input
      type="number"
      name="workoutID"
      onChange={(id) => handleWorkoutID(id)}
      placeholder="workout id"
      />
      <input
        type="text"
        value={exerciseName}
        onChange={handleNameChange}
        placeholder="Exercise Name"
      />
      {sets.map((set, index) => (
        <div key={index}>
          <input
            type="number"
            name="weight"
            value={set.weight}
            onChange={(e) => handleSetInput(index, e)}
            placeholder="Weight"
          />
          <input
            type="number"
            name="reps"
            value={set.reps}
            onChange={(e) => handleSetInput(index, e)}
            placeholder="Reps"
          />
          <button onClick={() => removeSet(index)}>Remove</button>
        </div>
      ))}
      <button onClick={addSet}>Add Set</button>
      <button onClick={submitSets}>Submit</button>
    </div>
  );
}

function App() {
  const [categories, setCategories] = useState([]);

  const fetchCategory = async () => {
    const cat_response = await axios.get("http://127.0.0.1:8000/categories/");
    console.log(cat_response.data);
    setCategories(cat_response.data);
  };

  const [alive, setStatus] = useState(null);
  // define a state to store the categories with an empty array
  const pingServer = async () => {
    const response = await axios.get("http://127.0.0.1:8000");
    setStatus(response.data);
  };

  return (
    <div className="App">
      <header className="App-header">       
        <button className="test-btn" onClick={pingServer}>
          ping server
        </button>
        {alive && (
          <div className="ping-status">
            response from API: {alive}
          </div>
        )}
        <button className="test-btn" onClick={fetchCategory}>
          fetch category
        </button>
        {categories.length > 0 && (
            <div className="ping-status">
                response from API:{" "}
                <ul className="category-info">
                  {categories.map((category) => (
                    <li key={category.id}> {category.id} {category.name}</li>
                  ))}
                </ul>
            </div>
          )}
        <SetInput />
      </header>
    </div>
  );
}

export default App;
