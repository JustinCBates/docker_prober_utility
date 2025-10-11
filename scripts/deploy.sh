#!/bin/bash
# Build and Deploy Docker Prober Utility
# This script builds the Docker image, runs it, collects host information,
# and outputs results to probe_data.json

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="prober"
CONTAINER_NAME="prober"
PROBE_DATA_FILE="$PROJECT_DIR/probe_data.json"

echo "==> Docker Prober Utility - Build and Deploy"
echo ""

# Step 1: Build the Docker image
echo "==> Step 1: Building Docker image..."
cd "$PROJECT_DIR"
docker build -t "$IMAGE_NAME" .
echo "✓ Docker image built successfully"
echo ""

# Step 2: Stop and remove existing container if running
echo "==> Step 2: Cleaning up existing containers..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
echo "✓ Cleanup complete"
echo ""

# Step 3: Run the Docker container
echo "==> Step 3: Starting Docker container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p 8080:8080 \
    --privileged \
    "$IMAGE_NAME"
echo "✓ Container started successfully"
echo ""

# Step 4: Wait for the app to be ready
echo "==> Step 4: Waiting for app to be ready..."
sleep 3
for i in {1..10}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✓ App is ready"
        break
    fi
    echo "  Waiting... ($i/10)"
    sleep 2
done
echo ""

# Step 5: Trigger host information collection
echo "==> Step 5: Collecting host information..."
if command -v jq &> /dev/null; then
    curl -s -X POST http://localhost:8080/collect | jq '.'
elif command -v python3 &> /dev/null; then
    curl -s -X POST http://localhost:8080/collect | python3 -m json.tool
else
    curl -s -X POST http://localhost:8080/collect
fi
sleep 2
echo "✓ Collection complete"
echo ""

# Step 6: Retrieve probe data
echo "==> Step 6: Retrieving probe data..."
if command -v jq &> /dev/null; then
    curl -s http://localhost:8080/probe | jq '.' > "$PROBE_DATA_FILE"
elif command -v python3 &> /dev/null; then
    curl -s http://localhost:8080/probe | python3 -m json.tool > "$PROBE_DATA_FILE"
else
    curl -s http://localhost:8080/probe > "$PROBE_DATA_FILE"
fi
echo "✓ Probe data saved to: $PROBE_DATA_FILE"
echo ""

# Step 7: Display summary
echo "==> Summary:"
echo "  - Container: $CONTAINER_NAME"
echo "  - Image: $IMAGE_NAME"
echo "  - Port: 8080"
echo "  - Data file: $PROBE_DATA_FILE"
echo ""
echo "Available endpoints:"
echo "  - http://localhost:8080/         (hello)"
echo "  - http://localhost:8080/health   (health check)"
echo "  - http://localhost:8080/probe    (view probe data)"
echo "  - http://localhost:8080/test     (test proxy/server)"
echo ""
echo "To view logs:"
echo "  docker logs $CONTAINER_NAME"
echo ""
echo "To stop and remove container:"
echo "  docker rm -f $CONTAINER_NAME"
echo ""
echo "✓ Deployment complete!"
