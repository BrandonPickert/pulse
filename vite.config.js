import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react(), {
    name: 'api-middleware',
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        if (req.url?.startsWith('/api')) {
          const { readData, writeData } = await import('./server/data.js');
          
          res.setHeader('Access-Control-Allow-Origin', '*');
          res.setHeader('Content-Type', 'application/json');
          
          try {
            if (req.url === '/api/workouts' && req.method === 'GET') {
              const data = await readData();
              res.end(JSON.stringify(data.workouts));
            } else if (req.url === '/api/stats' && req.method === 'GET') {
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
              res.end(JSON.stringify(stats));
            } else if (req.url === '/api/workouts' && req.method === 'POST') {
              let body = '';
              req.on('data', chunk => body += chunk);
              req.on('end', async () => {
                const data = await readData();
                const newWorkout = {
                  id: Date.now().toString(),
                  ...JSON.parse(body),
                  createdAt: new Date().toISOString()
                };
                data.workouts.push(newWorkout);
                await writeData(data);
                res.statusCode = 201;
                res.end(JSON.stringify(newWorkout));
              });
            } else if (req.url?.startsWith('/api/workouts/') && req.method === 'DELETE') {
              const id = req.url.split('/').pop();
              const data = await readData();
              data.workouts = data.workouts.filter(w => w.id !== id);
              await writeData(data);
              res.end(JSON.stringify({ success: true }));
            } else {
              next();
            }
          } catch (error) {
            console.error('API Error:', error);
            res.statusCode = 500;
            res.end(JSON.stringify({ error: 'Server error' }));
          }
        } else {
          next();
        }
      });
    }
  }],
  server: {
    host: '0.0.0.0',
    port: 5000
  }
});
