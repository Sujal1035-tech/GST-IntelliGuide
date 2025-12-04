# Docker Deployment Guide for GST-IntelliGuide

This guide provides step-by-step instructions to deploy the GST-IntelliGuide application using Docker and Docker Compose.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Docker** (version 20.10 or higher)
   - Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - Linux: [Docker Engine](https://docs.docker.com/engine/install/)
   - macOS: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

2. **Docker Compose** (version 2.0 or higher)
   - Included with Docker Desktop
   - Linux: Install separately if needed

Verify installation:
```bash
docker --version
docker-compose --version
```

## Step-by-Step Deployment

### Step 1: Clone the Repository (if not already done)

```bash
git clone <your-repository-url>
cd gst_bot
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your actual values:
   ```bash
   # On Windows
   notepad .env
   
   # On Linux/Mac
   nano .env
   ```

3. **Required Configuration:**
   - `SECRET_KEY`: Generate a secure random string (e.g., use `openssl rand -hex 32`)
   - `GROQ_API_KEY`: Your Groq API key from https://console.groq.com/
   - `MONGO_URI`: Keep default for Docker MongoDB, or use external MongoDB URI
   - `DB_NAME`: Database name (default: `gst_bot`)

> [!IMPORTANT]
> **For Production**: Always use strong, unique values for `SECRET_KEY` and `MONGO_ROOT_PASSWORD`

### Step 3: Build the Docker Image

Build the application image:
```bash
docker-compose build
```

This process may take several minutes as it:
- Downloads the Python base image
- Installs system dependencies
- Installs Python packages from `requirements.txt`
- Copies your application code

### Step 4: Start the Services

Start all services in detached mode:
```bash
docker-compose up -d
```

This will start:
- MongoDB database container
- GST-IntelliGuide application container

### Step 5: Verify Deployment

1. **Check container status:**
   ```bash
   docker-compose ps
   ```
   
   You should see both containers running:
   - `gst-mongodb`
   - `gst-intelliguide`

2. **View logs:**
   ```bash
   # All services
   docker-compose logs
   
   # Specific service
   docker-compose logs app
   docker-compose logs mongodb
   
   # Follow logs in real-time
   docker-compose logs -f app
   ```

3. **Check health status:**
   ```bash
   docker-compose ps
   ```
   Look for "healthy" status in the STATE column.

### Step 6: Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

You should see the login page of the GST-IntelliGuide application.

## Common Operations

### Stop the Services
```bash
docker-compose stop
```

### Start Stopped Services
```bash
docker-compose start
```

### Restart Services
```bash
docker-compose restart
```

### Stop and Remove Containers
```bash
docker-compose down
```

### Stop and Remove Containers + Volumes (⚠️ Deletes all data)
```bash
docker-compose down -v
```

### View Real-time Logs
```bash
docker-compose logs -f
```

### Execute Commands Inside Container
```bash
# Access app container shell
docker-compose exec app bash

# Access MongoDB shell
docker-compose exec mongodb mongosh -u admin -p password123
```

### Rebuild After Code Changes
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### Issue: Container fails to start

**Solution:**
1. Check logs: `docker-compose logs app`
2. Verify environment variables in `.env` file
3. Ensure ports 8000 and 27017 are not in use:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   netstat -ano | findstr :27017
   
   # Linux/Mac
   lsof -i :8000
   lsof -i :27017
   ```

### Issue: MongoDB connection failed

**Solution:**
1. Verify MongoDB is healthy: `docker-compose ps`
2. Check MongoDB logs: `docker-compose logs mongodb`
3. Ensure `MONGO_URI` in `.env` matches the MongoDB service configuration
4. Wait for MongoDB to fully initialize (can take 30-60 seconds on first run)

### Issue: Application shows "Internal Server Error"

**Solution:**
1. Check application logs: `docker-compose logs app`
2. Verify all required environment variables are set in `.env`
3. Ensure `GROQ_API_KEY` is valid
4. Check if MongoDB is accessible from the app container:
   ```bash
   docker-compose exec app ping mongodb
   ```

### Issue: Port already in use

**Solution:**
1. Change the port mapping in `docker-compose.yml`:
   ```yaml
   ports:
     - "8080:8000"  # Use 8080 instead of 8000
   ```
2. Rebuild and restart: `docker-compose up -d`

### Issue: Out of disk space

**Solution:**
1. Remove unused Docker resources:
   ```bash
   docker system prune -a
   docker volume prune
   ```

## Production Deployment Considerations

### Security

1. **Use strong credentials:**
   - Generate secure `SECRET_KEY`: `openssl rand -hex 32`
   - Use strong MongoDB passwords
   - Never commit `.env` file to version control

2. **Use HTTPS:**
   - Set up a reverse proxy (nginx, Traefik)
   - Obtain SSL certificates (Let's Encrypt)

3. **Network security:**
   - Don't expose MongoDB port (27017) publicly
   - Use firewall rules
   - Consider using Docker secrets for sensitive data

### Performance

1. **Resource limits:**
   Add to `docker-compose.yml`:
   ```yaml
   services:
     app:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
           reservations:
             cpus: '1'
             memory: 2G
   ```

2. **Use external MongoDB:**
   - For production, consider managed MongoDB (MongoDB Atlas, AWS DocumentDB)
   - Update `MONGO_URI` in `.env`
   - Remove MongoDB service from `docker-compose.yml`

### Monitoring

1. **Health checks:**
   - Already configured in `docker-compose.yml`
   - Monitor with: `docker-compose ps`

2. **Logging:**
   - Configure log rotation
   - Use centralized logging (ELK stack, CloudWatch)

### Backup

1. **Database backup:**
   ```bash
   # Backup MongoDB
   docker-compose exec mongodb mongodump --out /data/backup
   
   # Copy backup to host
   docker cp gst-mongodb:/data/backup ./mongodb-backup
   ```

2. **Volume backup:**
   ```bash
   docker run --rm -v gst_bot_mongodb_data:/data -v $(pwd):/backup ubuntu tar czf /backup/mongodb-backup.tar.gz /data
   ```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGO_URI` | Yes | `mongodb://admin:password123@mongodb:27017/` | MongoDB connection string |
| `DB_NAME` | Yes | `gst_bot` | Database name |
| `SECRET_KEY` | Yes | - | JWT secret key for authentication |
| `TOKEN_EXPIRE_MINUTES` | No | `60` | JWT token expiration time in minutes |
| `GROQ_API_KEY` | Yes | - | Groq API key for AI features |
| `HF_EMBEDDING_MODEL` | No | `sentence-transformers/all-MiniLM-L6-v2` | HuggingFace embedding model |
| `MONGO_ROOT_USERNAME` | No | `admin` | MongoDB root username (Docker only) |
| `MONGO_ROOT_PASSWORD` | No | `password123` | MongoDB root password (Docker only) |

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)

## Support

If you encounter issues not covered in this guide:
1. Check the application logs: `docker-compose logs app`
2. Check MongoDB logs: `docker-compose logs mongodb`
3. Verify your `.env` configuration
4. Ensure all prerequisites are installed correctly
