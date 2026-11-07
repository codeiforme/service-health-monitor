#!/usr/bin/env bash
set -e

if [ "${1:-}" = "down" ]; then
    kubectl -n health-monitor exec deployment/target -- touch /tmp/unhealthy
elif [ "${1:-}" = "up" ]; then
    kubectl -n health-monitor exec deployment/target -- rm -f /tmp/unhealthy
else
    echo "Usage: bash scripts/kubernetes-demo.sh down|up"
    exit 1
fi
