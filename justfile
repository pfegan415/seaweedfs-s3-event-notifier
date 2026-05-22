
run-local:
    uv run granian --interface asgi seaweedfs_s3_event_notifier/main.py

test:
    uv run pytest