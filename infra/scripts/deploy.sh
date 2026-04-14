#!/bin/bash
set -e

# ===========================================
# AudioBook Player Deployment Script
# ===========================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.prod.yml"
ENV_FILE="$SCRIPT_DIR/.env"

# Default values
BACKUP_DIR="$SCRIPT_DIR/backups"
LOG_FILE="$SCRIPT_DIR/deploy.log"
IMAGE_TAG="latest"

# ===========================================
# Functions
# ===========================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}

check_requirements() {
    log_info "Checking requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check .env file
    if [ ! -f "$ENV_FILE" ]; then
        log_warn ".env file not found, using .env.example as template"
        cp "$SCRIPT_DIR/.env.example" "$ENV_FILE"
        log_error "Please edit $ENV_FILE with your configuration"
        exit 1
    fi
    
    log_info "All requirements met"
}

backup_database() {
    log_info "Creating database backup..."
    
    BACKUP_NAME="audioplayer_backup_$(date +%Y%m%d_%H%M%S).sql"
    BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
    
    mkdir -p "$BACKUP_DIR"
    
    # Use docker to run pg_dump
    docker-compose -f "$COMPOSE_FILE" exec -T db pg_dump -U audioplayer audioplayer > "$BACKUP_PATH" || {
        log_warn "Backup failed, continuing anyway..."
        return 0
    }
    
    log_info "Database backup saved to: $BACKUP_PATH"
    
    # Keep only last 7 backups
    ls -t "$BACKUP_DIR"/*.sql | tail -n +8 | xargs -r rm -f
    log_info "Old backups cleaned up"
}

pull_images() {
    log_info "Pulling latest images..."
    
    # Build or pull images
    docker-compose -f "$COMPOSE_FILE" build --no-cache backend frontend
    
    log_info "Images built successfully"
}

deploy() {
    log_info "Starting deployment..."
    
    # Stop existing containers
    docker-compose -f "$COMPOSE_FILE" down
    
    # Start services
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log_info "Waiting for services to be healthy..."
    
    # Wait for backend to be healthy
    for i in {1..30}; do
        if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            log_info "Backend is healthy"
            break
        fi
        sleep 2
    done
    
    # Wait for nginx to be healthy
    for i in {1..10}; do
        if curl -sf http://localhost/health > /dev/null 2>&1; then
            log_info "Nginx is healthy"
            break
        fi
        sleep 2
    done
    
    log_info "Deployment completed successfully"
}

rollback() {
    log_warn "Rolling back to previous version..."

    # Find the most recent backup
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/*.sql 2>/dev/null | head -n1)

    if [ -z "$LATEST_BACKUP" ]; then
        log_error "No backup found for rollback"
        log_error "Please ensure backups exist in $BACKUP_DIR"
        exit 1
    fi

    log_info "Using backup: $LATEST_BACKUP"

    # Stop services
    log_info "Stopping services..."
    docker-compose -f "$COMPOSE_FILE" down

    # Start database only
    log_info "Starting database for restore..."
    docker-compose -f "$COMPOSE_FILE" up -d db

    # Wait for database to be ready
    log_info "Waiting for database..."
    sleep 10

    # Drop existing connections and restore
    log_info "Restoring database from backup..."
    docker-compose -f "$COMPOSE_FILE" exec -T db psql -U audioplayer -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'audioplayer' AND pid <> pg_backend_pid();" 2>/dev/null || true
    docker-compose -f "$COMPOSE_FILE" exec -T db psql -U audioplayer -d postgres -c "DROP DATABASE IF EXISTS audioplayer;" 2>/dev/null || true
    docker-compose -f "$COMPOSE_FILE" exec -T db psql -U audioplayer -d postgres -c "CREATE DATABASE audioplayer;" 2>/dev/null || true

    # Restore from backup
    cat "$LATEST_BACKUP" | docker-compose -f "$COMPOSE_FILE" exec -T db psql -U audioplayer audioplayer

    if [ $? -eq 0 ]; then
        log_info "Database restored successfully"
    else
        log_error "Database restore failed"
        exit 1
    fi

    # Start all services
    log_info "Starting all services..."
    docker-compose -f "$COMPOSE_FILE" up -d

    log_info "Rollback completed successfully"
    log_info "Restored from: $LATEST_BACKUP"
}

show_status() {
    log_info "Service status:"
    docker-compose -f "$COMPOSE_FILE" ps
}

show_logs() {
    SERVICE=${1:-}
    if [ -n "$SERVICE" ]; then
        docker-compose -f "$COMPOSE_FILE" logs -f --tail=100 "$SERVICE"
    else
        docker-compose -f "$COMPOSE_FILE" logs -f --tail=50
    fi
}

# ===========================================
# Main Script
# ===========================================

# Parse command line arguments
COMMAND=${1:-deploy}

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

log_info "Starting AudioBook Player deployment script"
log_info "Command: $COMMAND"

case "$COMMAND" in
    deploy)
        check_requirements
        backup_database
        pull_images
        deploy
        show_status
        ;;
    start)
        docker-compose -f "$COMPOSE_FILE" up -d
        show_status
        ;;
    stop)
        docker-compose -f "$COMPOSE_FILE" down
        ;;
    restart)
        docker-compose -f "$COMPOSE_FILE" restart
        show_status
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs ${2:-}
        ;;
    backup)
        backup_database
        ;;
    rollback)
        rollback
        ;;
    *)
        echo "Usage: $0 {deploy|start|stop|restart|status|logs|backup|rollback}"
        echo ""
        echo "Commands:"
        echo "  deploy   - Full deployment (default)"
        echo "  start    - Start services"
        echo "  stop     - Stop services"
        echo "  restart  - Restart services"
        echo "  status   - Show service status"
        echo "  logs     - Show logs (optional: service name)"
        echo "  backup   - Create database backup"
        echo "  rollback - Rollback to previous version"
        exit 1
        ;;
esac

log_info "Script completed"
