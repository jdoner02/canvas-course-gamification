#!/bin/bash

# Linear Algebra Course Builder - Setup and Run Script
# ===================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_status "Python version: $python_version"
    
    # Check pip
    if ! command_exists pip3; then
        print_error "pip3 is required but not installed."
        exit 1
    fi
    
    print_success "System requirements check passed"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Setup environment configuration
setup_environment() {
    print_status "Setting up environment configuration..."
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        cat > .env << EOF
# Canvas API Configuration
CANVAS_API_URL=https://canvas.instructure.com
CANVAS_API_TOKEN='your-canvas-api-token-here'

# Flask Configuration
FLASK_SECRET_KEY='$(python3 -c "import secrets; print(secrets.token_hex(32))")'
DEBUG=false
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Optional Configuration
HTTPS_ENABLED=false
EOF
        print_warning "Please update .env file with your Canvas API token before running the server"
    fi
    
    # Check for encryption key
    if [ ! -d "config" ]; then
        mkdir -p config
    fi
    
    if [ ! -f "config/.privacy_encryption_key" ]; then
        print_status "Generating encryption key..."
        python3 -c "
from cryptography.fernet import Fernet
key = Fernet.generate_key()
with open('config/.privacy_encryption_key', 'wb') as f:
    f.write(key)
print('Encryption key generated successfully')
"
    fi
    
    # Create necessary directories
    mkdir -p logs
    mkdir -p uploads
    mkdir -p exports
    mkdir -p data
    
    print_success "Environment setup completed"
}

# Initialize database
initialize_database() {
    print_status "Initializing database..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Initialize the database through the template manager
    python3 -c "
from src.course_templates.linear_algebra_template import LinearAlgebraTemplateManager
manager = LinearAlgebraTemplateManager()
print('Database initialized successfully')
"
    
    print_success "Database initialization completed"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run basic validation tests
    python3 -c "
import sys
sys.path.insert(0, '.')

# Test imports
try:
    from app import app
    from src.course_templates.linear_algebra_template import LinearAlgebraTemplateManager
    print('✅ All imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)

# Test Flask app configuration
try:
    with app.test_client() as client:
        response = client.get('/')
        if response.status_code == 200:
            print('✅ Flask app responding correctly')
        else:
            print(f'❌ Flask app error: status {response.status_code}')
            sys.exit(1)
except Exception as e:
    print(f'❌ Flask app test failed: {e}')
    sys.exit(1)

print('✅ All tests passed')
"
    
    print_success "Tests completed successfully"
}

# Start the server
start_server() {
    print_status "Starting Linear Algebra Course Builder server..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Check environment variables
    if [ -f ".env" ]; then
        export $(cat .env | xargs)
    fi
    
    # Start the server
    python3 server.py
}

# Display help
show_help() {
    echo "Linear Algebra Course Builder - Setup and Run Script"
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     - Install dependencies and setup environment"
    echo "  install   - Install Python dependencies only"
    echo "  init      - Initialize database"
    echo "  test      - Run validation tests"
    echo "  start     - Start the server"
    echo "  dev       - Start in development mode"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup     # Full setup (recommended for first run)"
    echo "  $0 start     # Start the server"
    echo "  $0 dev       # Development mode with debug enabled"
}

# Development mode
start_dev() {
    print_status "Starting in development mode..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Set development environment
    export DEBUG=true
    export LOG_LEVEL=DEBUG
    
    # Check environment variables
    if [ -f ".env" ]; then
        export $(cat .env | xargs)
    fi
    
    print_status "Development server starting with debug mode enabled"
    python3 server.py
}

# Main script logic
main() {
    echo ""
    echo "🧮 Linear Algebra Course Builder"
    echo "=================================="
    echo ""
    
    case "${1:-help}" in
        "setup")
            check_requirements
            install_dependencies
            setup_environment
            initialize_database
            run_tests
            print_success "Setup completed! Run './run.sh start' to start the server."
            ;;
        "install")
            check_requirements
            install_dependencies
            ;;
        "init")
            initialize_database
            ;;
        "test")
            run_tests
            ;;
        "start")
            check_requirements
            start_server
            ;;
        "dev")
            check_requirements
            start_dev
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"
