import React, { useState, useEffect } from "react";
import axios from "axios";

function SetInput({baseWorkoutID}) {
//   const [exerciseName, setName] = useState("");
  const [sets, setSets] = useState([{ weight: "", reps: "" }]);
  const [workoutID, setWorkoutID] = useState(baseWorkoutID);

  // dropdowns
  const [categories, setCategories] = useState([]);
  const [exercises, setExercises] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedExercise, setSelectedExercise] = useState("");


  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    if (selectedCategory) {
      fetchExercises(selectedCategory);
    }
  }, [selectedCategory]);

  useEffect(() => {
    setWorkoutID(baseWorkoutID);
  }, [baseWorkoutID])

  const fetchCategories = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/categories/");
      setCategories(response.data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  const fetchExercises = async (categoryID) => {
    try {
        console.log(categoryID)
      const response = await axios.get(`http://127.0.0.1:8000/categories/${categoryID}/exercises`);
      setExercises(response.data);
    } catch (error) {
      console.error("Error fetching exercises:", error);
    }
  };

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setSelectedExercise(""); // Reset selected exercise when category changes
  };

  const handleExerciseChange = (event) => {
    setSelectedExercise(event.target.value);
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
        name: selectedExercise,
        set_info: formattedSets,
      };

      console.log("Formatted sets:", exerciseData);
      const response = await axios.post(
        "http://127.0.0.1:8000/entries/",
        exerciseData
      );
      console.log("Exercises logged:", response.data);
      // clearrrrrrr
      setSelectedExercise("");
      setSets([{ weight: "", reps: "" }]);
    } catch (error) {
      console.error("Error logging exercises:", error);
    }
  };

  return (
    <div className="set-input">
      <div className="set-row">
      <input
        type="number"
        name="workoutID"
        onChange={(id) => handleWorkoutID(id)}
        placeholder="workout id"
        className="input-box"
      />
      <select
        value={selectedCategory}
        onChange={handleCategoryChange}
        className="input-box"
      >
        <option value="">Select Category</option>
        {categories.map((category) => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>
      <select
        value={selectedExercise}
        onChange={handleExerciseChange}
        className="input-box"
        disabled={!selectedCategory}
      >
        <option value="">Select Exercise</option>
        {exercises.map((exercise) => (
          <option key={exercise.id} value={exercise.name}>
            {exercise.name}
          </option>
        ))}
      </select>
      </div>
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

export default SetInput;
