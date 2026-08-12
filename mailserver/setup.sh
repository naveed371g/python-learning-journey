#!/usr/bin/env bash
#
# Convenience wrapper around the docker-mailserver `setup` CLI.
# Usage examples:
#   ./setup.sh email add user@example.com 'strong-password'
#   ./setup.sh email list
#   ./setup.sh alias add postmaster@example.com user@example.com
#   ./setup.sh config dkim
#   ./setup.sh help
#
# Anything you pass is forwarded to the setup command inside the container.

set -euo pipefail

CONTAINER="${DMS_CONTAINER:-mailserver}"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "Container '${CONTAINER}' is not running. Start it first with:"
  echo "  docker compose up -d"
  exit 1
fi

docker exec -ti "${CONTAINER}" setup "$@"
