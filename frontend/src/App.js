import axios from "axios";
import React, { useState } from "react";
import "./App.css";
import SetInput from "./Input";

function App() {
  const [alive, setStatus] = useState(null); // ping
  const [newWorkout, createNewWorkout] = useState('Unnamed Workout');// create new workout
  const [newWorkoutID, setNewWorkoutID] = useState(null);

  const createWorkout = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/workouts/', {
        name: newWorkout
      });
      console.log('New workout created:', response.data);
      createNewWorkout(''); // Clear the input field
    } catch (error) {
      console.error('Error creating workout:', error);
      alert('Failed to create workout. Please try again.');
    }
    const workout_id_resp = await axios.get('http://127.0.0.1:8000/workouts/newest');
    setNewWorkoutID(workout_id_resp.data);
    // alert("Workout created with ID: " + workout_id_resp.data);
  };

  // define a state to store the categories with an empty array
  const pingServer = async () => {
    const resp = await axios.get("http://127.0.0.1:8000");
    setStatus(resp.data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="title">ZHUANG</div>
        <div className="top-section">
          <div className="create-workout">
              <input
                type="text"
                value={newWorkout}
                onChange={(e) => createNewWorkout(e.target.value)}
                placeholder="new workout"
                className="workout-input"
              />
              <button className="fetch-api-btn" onClick={createWorkout}>
                Create Workout
              </button>
              {newWorkoutID && (
                <div> Created ID: {newWorkoutID} </div>
              )}

          </div>
        </div>

        <SetInput />
        <button className="fetch-api-btn" onClick={pingServer}>
          ping server
        </button>
        {alive && (
          <div className="api-response-info">response from API: {alive}</div>
        )}
      </header>
    </div>
  );
}

export default App;
