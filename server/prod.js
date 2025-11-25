import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readData, writeData } from './data.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.get('/api/workouts', async (req, res) => {
  try {
    const data = await readData();
    res.json(data.workouts);
  } catch (error) {
    console.error('Error fetching workouts:', error);
    res.status(500).json({ error: 'Failed to fetch workouts' });
  }
});

app.post('/api/workouts', async (req, res) => {
  try {
    const data = await readData();
    const newWorkout = {
      id: Date.now().toString(),
      ...req.body,
      createdAt: new Date().toISOString()
    };
    data.workouts.push(newWorkout);
    await writeData(data);
    res.status(201).json(newWorkout);
  } catch (error) {
    console.error('Error creating workout:', error);
    res.status(500).json({ error: 'Failed to create workout' });
  }
});

app.delete('/api/workouts/:id', async (req, res) => {
  try {
    const data = await readData();
    data.workouts = data.workouts.filter(w => w.id !== req.params.id);
    await writeData(data);
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting workout:', error);
    res.status(500).json({ error: 'Failed to delete workout' });
  }
});

app.get('/api/stats', async (req, res) => {
  try {
    const data = await readData();
    const stats = {
      totalWorkouts: data.workouts.length,
      totalMinutes: data.workouts.reduce((sum, w) => sum + (w.duration || 0), 0),
      thisWeek: data.workouts.filter(w => {
        const date = new Date(w.createdAt);
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);
        return date > weekAgo;
      }).length
    };
    res.json(stats);
  } catch (error) {
    console.error('Error fetching stats:', error);
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
});

app.use(express.static(join(__dirname, '..', 'dist')));

app.get('*', (req, res) => {
  res.sendFile(join(__dirname, '..', 'dist', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Production server running on http://0.0.0.0:${PORT}`);
});
