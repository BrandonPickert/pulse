import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 3001;
const DATA_FILE = join(__dirname, '..', 'data', 'workouts.json');

app.use(cors());
app.use(express.json());

async function ensureDataFile() {
  try {
    await fs.access(DATA_FILE);
  } catch {
    await fs.mkdir(join(__dirname, '..', 'data'), { recursive: true });
    await fs.writeFile(DATA_FILE, JSON.stringify({ workouts: [], users: [] }));
  }
}

async function readData() {
  await ensureDataFile();
  const data = await fs.readFile(DATA_FILE, 'utf-8');
  return JSON.parse(data);
}

async function writeData(data) {
  await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2));
}

app.get('/api/workouts', async (req, res) => {
  try {
    const data = await readData();
    res.json(data.workouts);
  } catch (error) {
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
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
});

app.listen(PORT, 'localhost', () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
