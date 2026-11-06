#!/usr/bin/env bash
set -e

if [ "${1:-}" = "down" ]; then
    docker compose exec -T target touch /tmp/unhealthy
elif [ "${1:-}" = "up" ]; then
    docker compose exec -T target rm -f /tmp/unhealthy
else
    echo "Usage: bash scripts/demo.sh down|up"
    exit 1
fi
