#!/bin/bash
# Invoice PDF Generator - Setup Script (Linux/Mac)
# Version: 1.0 (Final)

echo "=============================================="
echo "Invoice PDF Generator - Setup"
echo "=============================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found!"
    echo "  Please install Docker Desktop:"
    echo "  https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ Docker found: $(docker --version)"
echo ""

# Check Docker is running
if ! docker info &> /dev/null; then
    echo "✗ Docker is not running!"
    echo "  Please start Docker Desktop"
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python3 not found (needed for invoice generation)"
    echo "   You can still build Docker image"
    echo ""
fi

# Build Docker image
echo "=============================================="
echo "Building Docker Image"
echo "=============================================="
echo ""
echo "Image name: carrox-invoice-pdf-generator"
echo "This may take 2-3 minutes..."
echo ""

docker build -t carrox-invoice-pdf-generator .

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Docker image built successfully!"
    echo ""
    echo "Image details:"
    docker images carrox-invoice-pdf-generator
    echo ""
    echo "=============================================="
    echo "Setup Complete!"
    echo "=============================================="
    echo ""
    echo "Test PDF generation:"
    echo "  python3 generate_invoice.py"
    echo ""
    echo "Or manually:"
    echo '  docker run --rm -v "$(pwd):/data" carrox-invoice-pdf-generator \'
    echo '    /data/sample.html /data/sample.pdf'
    echo ""
    echo "For more information, see README.md"
    echo ""
else
    echo ""
    echo "✗ Docker build failed!"
    echo "  Check error messages above"
    exit 1
fi
