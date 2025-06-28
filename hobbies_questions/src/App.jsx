import { useState } from 'react';

// Elastic Beanstalk backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function App() {
  const [form, setForm] = useState({ name: '', age: '', hobby: '', inspiration: '' });
  const [message, setMessage] = useState('');
  const [submissions, setSubmissions] = useState([]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE_URL}/entries`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        setMessage('Submission received!');
        setForm({ name: '', age: '', hobby: '', inspiration: '' });
      } else {
        setMessage('Failed to submit.');
      }
    } catch (err) {
      console.error(err);
      setMessage('Could not connect to server.');
    }
  };

  const fetchSubmissions = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/entries`);
      const json = await res.json();
      setSubmissions(json);
    } catch (err) {
      console.error('Error loading data:', err);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h2>My Creative Hobbies Poll</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="name"
          placeholder="Your Name"
          value={form.name}
          onChange={handleChange}
          required
        />
        <br /><br />
        <input
          name="age"
          placeholder="Your Age"
          value={form.age}
          onChange={handleChange}
          required
        />
        <br /><br />
        <input
          name="hobby"
          placeholder="Favorite Creative Hobby"
          value={form.hobby}
          onChange={handleChange}
          required
        />
        <br /><br />
        <textarea
          name="inspiration"
          placeholder="What inspires you?"
          value={form.inspiration}
          onChange={handleChange}
          required
        />
        <br /><br />
        <button type="submit">Submit</button>
      </form>

      {message && <p>{message}</p>}

      <br />
      <button onClick={fetchSubmissions}>View All Entries</button>

      {submissions.length > 0 && (
        <ul style={{ marginTop: '1rem' }}>
          {submissions.map((entry, index) => (
            <li key={index}>
              <strong>{entry.name}</strong> (Age: {entry.age ?? 'N/A'}) loves <em>{entry.hobby}</em> — "{entry.inspiration}"
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
