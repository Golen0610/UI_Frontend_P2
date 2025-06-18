import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    study_hours: '',
    sleep_hours: '',
    attendance: '',
    participation: ''
  });

  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult('');
    setError('');

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          study_hours: parseFloat(formData.study_hours),
          sleep_hours: parseFloat(formData.sleep_hours),
          attendance: parseFloat(formData.attendance),
          participation: parseFloat(formData.participation)
        })
      });

      const data = await response.json();

      if (response.ok) {
        setResult(`🎉 Prediction: ${data.result}`);
      } else {
        setError(`❌ Error: ${data.error}`);
      }
    } catch (err) {
      setError('🚨 Server error or Flask backend is not running.');
    }
  };

  return (
    <div className="container">
      <h1>📘 Student Pass/Fail Predictor</h1>
      <form onSubmit={handleSubmit}>
        <label>📚 Study Hours:</label>
        <input
          type="number"
          step="0.1"
          id="study_hours"
          value={formData.study_hours}
          onChange={handleChange}
          required
        />

        <label>🛌 Sleep Hours:</label>
        <input
          type="number"
          step="0.1"
          id="sleep_hours"
          value={formData.sleep_hours}
          onChange={handleChange}
          required
        />

        <label>🎓 Attendance (%):</label>
        <input
          type="number"
          step="1"
          id="attendance"
          value={formData.attendance}
          onChange={handleChange}
          required
        />

        <label>🙋 Participation (%):</label>
        <input
          type="number"
          step="1"
          id="participation"
          value={formData.participation}
          onChange={handleChange}
          required
        />

        <button type="submit">Predict Result</button>
      </form>

      {result && <div className="result-box success">{result}</div>}
      {error && <div className="result-box error">{error}</div>}
    </div>
  );
}

export default App;
