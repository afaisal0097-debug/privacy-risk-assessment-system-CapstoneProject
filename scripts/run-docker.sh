#!/usr/bin/env zsh
# Helper script to run the project's Docker Compose stack on macOS (zsh)
# Usage: ./scripts/run-docker.sh up|down|logs

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_CMD="docker compose"

usage() {
  echo "Usage: $0 up|down|logs"
  echo "  up    - build images and start containers in detached mode"
  echo "  down  - stop and remove containers and networks (keeps volumes)"
  echo "  logs  - show recent logs for all services (use -f to follow)"
  exit 2
}

if [[ "$#" -lt 1 ]]; then
  usage
fi

ACTION="$1"

check_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "Error: docker command not found. Please install Docker Desktop for macOS: https://www.docker.com/products/docker-desktop"
    exit 1
  fi

  if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker daemon not running. Please start Docker Desktop and try again."
    exit 1
  fi
}

cd "$ROOT_DIR"

case "$ACTION" in
  up)
    check_docker
    echo "Building and starting containers (detached)..."
    $COMPOSE_CMD up --build -d
    echo
    echo "Current containers:"
    docker ps --format 'table {{.Names}}	{{.Image}}	{{.Status}}	{{.Ports}}'
    echo
    echo "To stream logs: docker compose logs -f"
    ;;

  down)
    check_docker
    echo "Stopping and removing containers..."
    $COMPOSE_CMD down
    ;;

  logs)
    check_docker
    # Show recent logs (200 lines) for quick debugging
    echo "Showing recent logs (200 lines) for all services..."
    $COMPOSE_CMD logs --tail=200
    ;;

  *)
    usage
    ;;
esac
