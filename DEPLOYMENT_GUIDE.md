# Deployment Guide for AI Research Assistant Enterprise

## Prerequisites

Before deploying, you'll need:

1. **API Keys**:
   - OpenAI API Key (for LLM functionality)
   - SerpAPI Key (for web search functionality)

2. **System Requirements**:
   - Docker and Docker Compose (for containerized deployment)
   - Or Python 3.9+ with pip (for direct deployment)

## Option 1: Docker Deployment (Recommended)

### Step 1: Set up environment variables

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
LOG_LEVEL=INFO
```

### Step 2: Build and run with Docker Compose

```bash
# Build and start the application
docker-compose up --build -d

# View logs
docker-compose logs -f
```

### Step 3: Access the application

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Option 2: Direct Python Deployment

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set environment variables

```bash
export OPENAI_API_KEY=your_openai_api_key_here
export SERPAPI_API_KEY=your_serpapi_key_here
```

### Step 3: Run the application

```bash
# Using uvicorn directly
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload

# Or using gunicorn for production
pip install gunicorn
gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Option 3: Cloud Deployment

### Deploy to Heroku

1. Install Heroku CLI
2. Create a Heroku app:
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your_openai_api_key_here
   heroku config:set SERPAPI_API_KEY=your_serpapi_key_here
   git push heroku main
   ```

### Deploy to AWS/GCP/Azure

The application can be deployed to any cloud platform that supports Docker containers or Python applications. Simply:

1. Set up the cloud environment
2. Deploy the Docker container or application code
3. Configure environment variables
4. Expose the application on port 8000

## Production Considerations

### Security
- Use HTTPS in production
- Implement authentication if needed
- Store secrets securely (not in environment variables in production)

### Scaling
- The application is designed to be stateless
- Multiple instances can be run behind a load balancer
- Session data is stored in memory but can be moved to Redis for multi-instance deployments

### Monitoring
- The application includes comprehensive logging
- Add application monitoring tools as needed
- Set up alerts for error rates and performance metrics

## API Usage

Once deployed, you can interact with the API using:

```bash
# Submit a research task
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain quantum computing in simple terms",
    "max_sources": 5,
    "include_citations": true
  }'

# Get research status
curl -X GET "http://localhost:8000/research/{session_id}"

# Get all research sessions
curl -X GET "http://localhost:8000/research"
```

## Troubleshooting

1. **API Keys Not Working**: Verify that environment variables are correctly set
2. **Port Already in Use**: Change the port in docker-compose.yml or uvicorn command
3. **Memory Issues**: Adjust the application configuration for your system's resources
4. **Rate Limits**: The application handles rate limiting through SerpAPI and OpenAI