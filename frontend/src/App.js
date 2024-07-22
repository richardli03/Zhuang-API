import axios from "axios";
import React, { useState } from "react";
import "./App.css";

function SetInput() {
  const [exerciseName, setName] = useState("");
  const [sets, setSets] = useState([{ weight: "", reps: "" }]);
  const [workoutID, setWorkoutID] = useState(null);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleWorkoutID = (id) => {
    setWorkoutID(id.target.value);
  };

  const handleSetInput = (index, event) => {
    const { name, value } = event.target;
    const newSets = [...sets];
    newSets[index][name] = value;
    setSets(newSets);
  };

  const addSet = () => {
    setSets([...sets, { weight: "", reps: "" }]);
  };

  const removeSet = (index) => {
    const newSets = sets.filter((_, i) => i !== index);
    setSets(newSets);
  };

  const submitSets = async () => {
    try {
      const formattedSets = sets
        .map((set) => ({
          weight: parseFloat(set.weight),
          reps: parseInt(set.reps, 10),
        }))
        .filter((set) => set.weight && set.reps); // Remove any incomplete sets

      const exerciseData = {
        workout_id: workoutID,
        name: exerciseName,
        set_info: formattedSets,
      };

      console.log("Formatted sets:", exerciseData);
      const response = await axios.post(
        "http://127.0.0.1:8000/entries/",
        exerciseData
      );
      console.log("Exercises logged:", response.data);
      // clearrrrrrr
      setName("");
      setSets([{ weight: "", reps: "" }]);
    } catch (error) {
      console.error("Error logging exercises:", error);
    }
  };

  return (
    <div className="set-input">
      <input
        type="number"
        name="workoutID"
        onChange={(id) => handleWorkoutID(id)}
        placeholder="workout id"
        className="input-box"
      />
      <input
        type="text"
        value={exerciseName}
        onChange={handleNameChange}
        placeholder="exercise name"
        className="input-box"
      />
      {sets.map((set, index) => (
        <div className="set-row" key={index}>
          <input
            type="number"
            name="weight"
            value={set.weight}
            onChange={(e) => handleSetInput(index, e)}
            placeholder="weight"
            className="input-box"
          />
          <input
            type="number"
            name="reps"
            value={set.reps}
            onChange={(e) => handleSetInput(index, e)}
            placeholder="reps"
            className="input-box"
          />
          <button className="set-btn" onClick={() => removeSet(index)}>
            Remove
          </button>
        </div>
      ))}
      <button className="set-btn" onClick={addSet}>
        Add Set
      </button>
      <button className="set-btn" onClick={submitSets}>
        Submit
      </button>
    </div>
  );
}

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
