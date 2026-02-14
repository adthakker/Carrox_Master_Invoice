#!/bin/bash
# Quick Build Script for Invoice PDF Generator

echo "=============================================="
echo "Invoice PDF Generator - Quick Setup"
echo "=============================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found. Please install Docker Desktop:"
    echo "  https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ Docker found: $(docker --version)"
echo ""

# Check Docker is running
if ! docker info &> /dev/null; then
    echo "✗ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Build image
echo "Building Docker image 'invoice-pdf-generator'..."
echo "This may take 2-3 minutes..."
echo ""

docker build -t invoice-pdf-generator .

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Docker image built successfully!"
    echo ""
    echo "Image info:"
    docker images invoice-pdf-generator
    echo ""
    echo "=============================================="
    echo "Setup Complete!"
    echo "=============================================="
    echo ""
    echo "You can now generate PDFs:"
    echo "  python generate_invoice.py"
    echo ""
    echo "Or programmatically:"
    echo "  from generate_invoice import generate_invoice_html"
    echo "  generate_invoice_html('data.json', generate_pdf=True)"
    echo ""
else
    echo ""
    echo "✗ Docker build failed"
    exit 1
fi
