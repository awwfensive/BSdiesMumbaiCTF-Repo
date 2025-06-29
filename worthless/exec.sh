#!/bin/bash

echo "🚀 Starting CTF Django Application with Security Restrictions..."

# Config
IMAGE_NAME="worthless"
CONTAINER_NAME="ctf-app"
HOST_PORT=8000
CONTAINER_PORT=8000
DB_FILE="sqlite3.db"

# Check if image exists
if ! docker images | awk '{print $1}' | grep -qw "$IMAGE_NAME"; then
    echo "❌ Error: Docker image '$IMAGE_NAME' not found!"
    echo "💡 Please build the image first using:"
    echo "   docker build -t $IMAGE_NAME ."
    exit 1
fi

# Stop and remove existing container if running
if docker ps -a --format '{{.Names}}' | grep -qw "$CONTAINER_NAME"; then
    echo "🛑 Removing old container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
fi

# Check if HOST_PORT is already in use
if ss -tuln | grep -q ":$HOST_PORT "; then
    echo "⚠️  Port $HOST_PORT is already in use. Trying fallback to 8080..."
    HOST_PORT=8080
fi

# Ensure DB file exists and is writable
if [ ! -f "$DB_FILE" ]; then
    echo "ℹ️  Creating blank SQLite database file..."
    touch "$DB_FILE"
fi

chmod 666 "$DB_FILE"

# Start container
docker run -d \
  --name "$CONTAINER_NAME" \
  --cap-drop=ALL \
  --cap-add=SETUID \
  --cap-add=SETGID \
  -v "$(pwd)":/app \
  --tmpfs /tmp:rw,noexec,nosuid,size=50m \
  --tmpfs /var/tmp:rw,noexec,nosuid,size=10m \
  --tmpfs /app/logs:rw,noexec,nosuid,size=10m \
  --security-opt no-new-privileges:true \
  --pids-limit 100 \
  --memory=256m \
  --cpus=0.5 \
  -p "$HOST_PORT:$CONTAINER_PORT" \
  "$IMAGE_NAME"


# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Container '$CONTAINER_NAME' started successfully!"
    echo "🌐 Access your app at: http://localhost:$HOST_PORT"
    echo ""
    echo "📋 Useful commands:"
    echo "🔍 View logs:       docker logs -f $CONTAINER_NAME"
    echo "🛑 Stop container:  docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME"
    echo "🔒 Test restrictions: docker exec $CONTAINER_NAME ls -la"
else
    echo "❌ Failed to start container"
    exit 1
fi
