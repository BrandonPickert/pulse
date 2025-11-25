import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [workouts, setWorkouts] = useState([]);
  const [stats, setStats] = useState({ totalWorkouts: 0, totalMinutes: 0, thisWeek: 0 });
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    type: '',
    duration: '',
    notes: '',
    username: ''
  });

  useEffect(() => {
    fetchWorkouts();
    fetchStats();
  }, []);

  const fetchWorkouts = async () => {
    try {
      const response = await fetch('/api/workouts');
      const data = await response.json();
      setWorkouts(data);
    } catch (error) {
      console.error('Error fetching workouts:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await fetch('/api/workouts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          duration: parseInt(formData.duration)
        })
      });
      setFormData({ type: '', duration: '', notes: '', username: '' });
      setShowForm(false);
      fetchWorkouts();
      fetchStats();
    } catch (error) {
      console.error('Error creating workout:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`/api/workouts/${id}`, { method: 'DELETE' });
      fetchWorkouts();
      fetchStats();
    } catch (error) {
      console.error('Error deleting workout:', error);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>💪 Pulse</h1>
        <p>Community workout tracker</p>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.totalWorkouts}</div>
          <div className="stat-label">Total Workouts</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.totalMinutes}</div>
          <div className="stat-label">Total Minutes</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.thisWeek}</div>
          <div className="stat-label">This Week</div>
        </div>
      </div>

      <div className="actions">
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Log Workout'}
        </button>
      </div>

      {showForm && (
        <form className="workout-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Your name"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            required
          />
          <select
            value={formData.type}
            onChange={(e) => setFormData({ ...formData, type: e.target.value })}
            required
          >
            <option value="">Select workout type</option>
            <option value="Running">Running</option>
            <option value="Cycling">Cycling</option>
            <option value="Swimming">Swimming</option>
            <option value="Weightlifting">Weightlifting</option>
            <option value="Yoga">Yoga</option>
            <option value="Other">Other</option>
          </select>
          <input
            type="number"
            placeholder="Duration (minutes)"
            value={formData.duration}
            onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
            required
            min="1"
          />
          <textarea
            placeholder="Notes (optional)"
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            rows="3"
          />
          <button type="submit" className="btn-primary">Save Workout</button>
        </form>
      )}

      <div className="workouts-list">
        <h2>Recent Workouts</h2>
        {workouts.length === 0 ? (
          <p className="empty-state">No workouts yet. Log your first one!</p>
        ) : (
          workouts.slice().reverse().map((workout) => (
            <div key={workout.id} className="workout-card">
              <div className="workout-header">
                <div>
                  <strong>{workout.username}</strong>
                  <span className="workout-type">{workout.type}</span>
                </div>
                <button className="btn-delete" onClick={() => handleDelete(workout.id)}>
                  Delete
                </button>
              </div>
              <div className="workout-details">
                <span>{workout.duration} minutes</span>
                <span>{new Date(workout.createdAt).toLocaleDateString()}</span>
              </div>
              {workout.notes && <p className="workout-notes">{workout.notes}</p>}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
