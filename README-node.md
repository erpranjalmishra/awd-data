# Arduino Sensor Dashboard - Node.js Version

A Node.js/Express equivalent of the Django Arduino sensor dashboard application.

## Features

- **Home Dashboard**: Simple HTML interface showing server status
- **API Endpoints**: 
  - `/api/` - Returns sensor data in JSON format
  - `/apidatasensor/` - Alternative endpoint for sensor data
  - `/health/` - Health check endpoint with system information
- **Security**: Helmet.js for security headers, CORS enabled
- **Production Ready**: Compression, error handling, environment configuration

## API Endpoints

### GET /
Returns HTML dashboard page

### GET /api/ or /apidatasensor/
Returns sensor data:
```json
{
  "status": "ok",
  "message": "API is working",
  "timestamp": "2025-09-19T06:57:43.000Z",
  "temperature": 25.5,
  "humidity": 60.0,
  "ph": 7.0,
  "tds": 150.0,
  "o2": 21.0,
  "deviceid": "vikaspal@123"
}
```

### GET /health/
Returns health status and system information:
```json
{
  "status": "healthy",
  "message": "Server is running",
  "timestamp": "2025-09-19T06:57:43.000Z",
  "request_info": {
    "method": "GET",
    "path": "/health/",
    "host": "localhost:3000",
    "user_agent": "Mozilla/5.0..."
  },
  "environment": {
    "debug": "false",
    "allowed_hosts": "localhost,127.0.0.1,awd-data-6.onrender.com",
    "node_version": "v18.17.0",
    "platform": "win32"
  }
}
```

## Local Development

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Start production server:
```bash
npm start
```

The server will run on `http://localhost:3000`

## Environment Variables

- `PORT`: Server port (default: 3000)
- `NODE_DEBUG`: Enable debug mode (default: true)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `NODE_ENV`: Environment (development/production)

## Deployment on Render

1. Use the `render-node.yaml` configuration file
2. Set environment variables in Render dashboard
3. Deploy from your Git repository

## Dependencies

- **express**: Web framework
- **cors**: Cross-origin resource sharing
- **helmet**: Security middleware
- **compression**: Response compression

## Differences from Django Version

- Uses Express.js instead of Django
- No database required (static sensor data)
- Simplified middleware stack
- Native JSON responses
- Built-in static file serving