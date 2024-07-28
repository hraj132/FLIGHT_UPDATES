import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [name, setName] = useState('');
  const [flightDetails, setFlightDetails] = useState('');
  const [mobileNumber, setMobileNumber] = useState('');
  const [flightStatus, setFlightStatus] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous error messages
    try {
      const response = await axios.post('http://localhost:5000/get-flight-status', {
        name,
        flightDetails,
        mobileNumber
      });
      setFlightStatus(response.data.status);
    } catch (error) {
      if (error.response && error.response.status === 404) {
        setError('Flight not found. Please check your flight details and try again.');
      } else {
        setError('An error occurred while fetching the flight status. Please try again later.');
      }
      setFlightStatus('');
    }
  };

  return (
    <div className="App">
      <h1>Flight Status Tracker</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>User Name:</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div>
          <label>Flight Number:</label>
          <input type="text" value={flightDetails} onChange={(e) => setFlightDetails(e.target.value)} required />
        </div>
        <div>
          <label>Mobile Number:</label>
          <input type="text" value={mobileNumber} onChange={(e) => setMobileNumber(e.target.value)} required />
        </div>
        <button type="submit">Get Flight Status</button>
      </form>
      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}
      {flightStatus && (
        <div className="status">
          <h2>Flight Status</h2>
          <p>{flightStatus}</p>
        </div>
      )}
    </div>
  );
};

export default App;
