#!/bin/bash

# FlaskEdit Deployment Setup Script
echo "FlaskEdit Deployment Setup"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git first."
    exit 1
fi

echo "Prerequisites check passed"

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads
mkdir -p temp_conversions
mkdir -p static

# Set proper permissions
chmod 755 uploads temp_conversions static

echo "Setup complete!"
echo ""
echo "To run the application:"
echo "python3 main.py"
echo ""
echo "Then open your browser to:"
echo "http://localhost:5000"
echo ""
echo "For production deployment, make sure to:"
echo "1. Set FLASK_ENV=production"
echo "2. Configure a proper secret key"
echo "3. Use a production WSGI server"
echo ""
echo "Your app will be ready!" 