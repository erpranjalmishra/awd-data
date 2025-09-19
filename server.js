const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');

const app = express();
const PORT = process.env.PORT || 3000;

// Environment configuration
const getEnv = (name, defaultValue = null) => {
  return process.env[name] || defaultValue;
};

const DEBUG = getEnv('NODE_DEBUG', 'true').toLowerCase() === 'true';
const ALLOWED_HOSTS = getEnv('ALLOWED_HOSTS', 'localhost,127.0.0.1,awd-data-6.onrender.com').split(',');

// Middleware
app.use(helmet({
  contentSecurityPolicy: false, // Disable for simplicity
  crossOriginEmbedderPolicy: false
}));
app.use(compression());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static files
app.use('/static', express.static('public'));

// Routes
app.get('/', (req, res) => {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Arduino Dashboard</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
      <h1>Arduino Dashboard</h1>
      <p>Server is running!</p>
      <p>Time: ${new Date().toISOString()}</p>
      <p>
        <a href="/api/">API</a> | 
        <a href="/apidatasensor/">API Data Sensor</a> | 
        <a href="/health/">Health</a>
      </p>
    </body>
    </html>
  `;
  res.send(html);
});

app.get('/api/', (req, res) => {
  res.json({
    status: 'ok',
    message: 'API is working',
    timestamp: new Date().toISOString(),
    temperature: 25.5,
    humidity: 60.0,
    ph: 7.0,
    tds: 150.0,
    o2: 21.0,
    deviceid: 'vikaspal@123'
  });
});

// Same endpoint as /api/ for compatibility
app.get('/apidatasensor/', (req, res) => {
  res.json({
    status: 'ok',
    message: 'API is working',
    timestamp: new Date().toISOString(),
    temperature: 25.5,
    humidity: 60.0,
    ph: 7.0,
    tds: 150.0,
    o2: 21.0,
    deviceid: 'vikaspal@123'
  });
});

app.get('/health/', (req, res) => {
  res.json({
    status: 'healthy',
    message: 'Server is running',
    timestamp: new Date().toISOString(),
    request_info: {
      method: req.method,
      path: req.path,
      host: req.get('host'),
      user_agent: req.get('user-agent') || 'unknown'
    },
    environment: {
      debug: getEnv('NODE_DEBUG', 'not_set'),
      allowed_hosts: getEnv('ALLOWED_HOSTS', 'not_set'),
      node_version: process.version,
      platform: process.platform
    }
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `The requested URL ${req.originalUrl} was not found on this server.`,
    timestamp: new Date().toISOString()
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: DEBUG ? err.message : 'Something went wrong',
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Arduino Dashboard server running on port ${PORT}`);
  console.log(`Environment: ${DEBUG ? 'development' : 'production'}`);
  console.log(`Allowed hosts: ${ALLOWED_HOSTS.join(', ')}`);
});

module.exports = app;