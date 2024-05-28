#!/bin/bash

# 서비스가 시작될 때까지 최대 30초 동안 대기
for i in {1..30}; do
    if curl -f http://localhost:5000; then
        echo "Service is up and running."
        exit 0
    else
        echo "Waiting for the service to start..."
        sleep 1
    fi
done

echo "Service did not start within the expected time."
exit 1
