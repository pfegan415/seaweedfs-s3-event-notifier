
run-local:
    uv run granian --interface asgi seaweedfs_s3_event_notifier/main.py

test:
    uv run pytest

build-image:
    docker build -t seaweedfs-s3-event-notifier:latest .

run-container:
    docker run \
    --name notifier \
    --network notifier-network \
    -p 8081:8081 \
    --rm \
    seaweedfs-s3-event-notifier:latest