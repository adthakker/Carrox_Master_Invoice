# Invoice PDF Generator - Docker Setup Guide

Complete setup guide for generating PDF invoices using WeasyPrint in Docker.

## 📋 Overview

This system generates professional invoice PDFs using:
- **Jinja2**: Template engine for HTML generation
- **WeasyPrint**: HTML to PDF conversion (runs in Docker)
- **Docker**: Isolated Linux environment for WeasyPrint

```
JSON Data → Jinja2 Template → HTML → Docker/WeasyPrint → PDF
```

## 🔧 Prerequisites

### 1. Docker Desktop
**Required**: Docker must be installed and running

**Download**: https://www.docker.com/products/docker-desktop

**Verify Installation**:
```bash
docker --version
# Should show: Docker version 24.x.x or higher
```

**Start Docker Desktop** before proceeding.

### 2. Python 3.x
**Required**: For running generate_invoice.py on your host system

**Install Dependencies**:
```bash
pip install jinja2
```

## 🚀 Quick Start

### Step 1: Build Docker Image

Navigate to your project directory and build the Docker image:

```bash
docker build -t invoice-pdf-generator .
```

**What this does**:
- Creates a Linux-based Docker image
- Installs WeasyPrint and all system dependencies
- Sets up the PDF conversion script
- Image size: ~400MB

**Build time**: 2-3 minutes (first time only)

### Step 2: Verify Image Built Successfully

```bash
docker images invoice-pdf-generator
```

Expected output:
```
REPOSITORY               TAG       IMAGE ID       CREATED          SIZE
invoice-pdf-generator    latest    abc123def456   2 minutes ago    400MB
```

### Step 3: Generate Invoice (HTML + PDF)

#### Option A: Programmatic Usage (Recommended)

```python
from generate_invoice import generate_invoice_html

# Generate both HTML and PDF
generate_invoice_html(
    json_data='sample_invoice_data.json',
    template_path='invoice_template.html',
    output_path='invoice.html',
    generate_pdf=True  # Enable PDF generation
)
```

#### Option B: Command Line

```bash
# Generate HTML only
python generate_invoice.py

# Then convert to PDF separately
python -c "from generate_invoice import convert_html_to_pdf; convert_html_to_pdf('generated_invoice.html')"
```

## 📁 Project Structure

```
your-project/
├── Dockerfile                   # Docker image definition
├── pdf_converter.py            # PDF conversion script (runs in container)
├── generate_invoice.py         # Main script (runs on host)
├── invoice_template.html       # Jinja2 template
├── sample_invoice_data.json    # Sample data
├── company_logo.jpeg          # Company logo
└── outputs/
    ├── invoice.html           # Generated HTML
    └── invoice.pdf            # Generated PDF
```

## 🐳 How It Works

### Architecture

```
┌──────────────────────────────────┐
│ HOST SYSTEM                       │
│ (Windows/Mac/Linux)              │
│                                  │
│ 1. generate_invoice.py           │
│    - Load JSON data              │
│    - Render Jinja2 template      │
│    - Save HTML file              │
│                                  │
│ 2. If generate_pdf=True:         │
│    - Call Docker container ──────┼──→ ┌────────────────────────┐
│                                  │    │ DOCKER CONTAINER       │
│ 3. Read generated PDF ←──────────┼────│ (Linux Environment)    │
│                                  │    │                        │
└──────────────────────────────────┘    │ - WeasyPrint + deps    │
                                        │ - pdf_converter.py     │
                                        │ - Converts HTML → PDF  │
                                        └────────────────────────┘
```

### Volume Mounting

Docker accesses files via volume mounting:

```bash
docker run --rm \
  -v /path/to/files:/data \
  invoice-pdf-generator \
  /data/invoice.html \
  /data/invoice.pdf
```

**What happens**:
1. Host directory is mounted as `/data` in container
2. Container reads HTML from `/data/invoice.html`
3. Container writes PDF to `/data/invoice.pdf`
4. PDF appears immediately in host directory

## 💻 Usage Examples

### Example 1: Generate Single Invoice

```python
from generate_invoice import generate_invoice_html

generate_invoice_html(
    json_data='invoice_data.json',
    output_path='output/invoice_001.html',
    generate_pdf=True
)
```

### Example 2: Batch Processing

```python
from generate_invoice import generate_invoice_html
import json

invoice_files = ['inv1.json', 'inv2.json', 'inv3.json']

for inv_file in invoice_files:
    with open(inv_file) as f:
        data = json.load(f)
    
    inv_num = data['invoice']['number']
    
    generate_invoice_html(
        json_data=data,
        output_path=f'output/{inv_num}.html',
        generate_pdf=True
    )
    
    print(f"✓ Generated {inv_num}")
```

### Example 3: Convert Existing HTML

```python
from generate_invoice import convert_html_to_pdf

# Convert existing HTML file to PDF
convert_html_to_pdf(
    html_path='existing_invoice.html',
    pdf_path='invoice.pdf'
)
```

### Example 4: Custom Docker Image Name

```python
from generate_invoice import convert_html_to_pdf

convert_html_to_pdf(
    html_path='invoice.html',
    pdf_path='invoice.pdf',
    docker_image='my-custom-pdf-generator'
)
```

## 🔍 Advanced Usage

### Manual Docker Command

Convert HTML to PDF manually:

```bash
docker run --rm \
  -v "$(pwd):/data" \
  invoice-pdf-generator \
  /data/invoice.html \
  /data/invoice.pdf
```

**Windows (PowerShell)**:
```powershell
docker run --rm -v "${PWD}:/data" invoice-pdf-generator /data/invoice.html /data/invoice.pdf
```

### Python Script with Error Handling

```python
from generate_invoice import generate_invoice_html, convert_html_to_pdf
import sys

try:
    # Generate HTML
    generate_invoice_html(
        json_data='data.json',
        output_path='invoice.html'
    )
    
    # Convert to PDF
    success = convert_html_to_pdf('invoice.html', 'invoice.pdf')
    
    if success:
        print("✓ Invoice PDF generated successfully!")
    else:
        print("✗ PDF generation failed")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
```

## 🛠️ Troubleshooting

### Issue: "Docker image not found"

**Symptom**:
```
✗ Error: Docker image 'invoice-pdf-generator' not found
```

**Solution**:
```bash
docker build -t invoice-pdf-generator .
```

### Issue: "Docker is not installed or not running"

**Solution**:
1. Install Docker Desktop: https://www.docker.com/products/docker-desktop
2. Start Docker Desktop application
3. Verify: `docker --version`

### Issue: Images not showing in PDF

**Problem**: Logo paths are incorrect

**Solution 1**: Keep images in same directory as HTML
```
output/
├── invoice.html
├── invoice.pdf
├── company_logo.jpeg
└── carrox_logo.png
```

**Solution 2**: Copy images to output directory before generation
```python
import shutil

# Copy logos
shutil.copy('company_logo.jpeg', 'output/')
shutil.copy('carrox_logo.png', 'output/')

# Generate invoice
generate_invoice_html(
    json_data='data.json',
    output_path='output/invoice.html',
    generate_pdf=True
)
```

### Issue: Permission denied (Windows)

**Solution**: Enable file sharing in Docker Desktop
1. Open Docker Desktop → Settings
2. Resources → File Sharing
3. Add your project directory
4. Click "Apply & Restart"

### Issue: PDF generation timeout

**Solution**: Increase timeout in generate_invoice.py

Find this line:
```python
result = subprocess.run(
    docker_cmd,
    capture_output=True,
    text=True,
    timeout=60  # Increase to 120
)
```

### Issue: Font warnings

**Symptom**: Warnings about missing fonts

**Solution**: Already handled in Dockerfile with `fonts-liberation`. For additional fonts:

```dockerfile
# Add to Dockerfile after other RUN commands
RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/*
```

Then rebuild:
```bash
docker build -t invoice-pdf-generator .
```

## ⚙️ Configuration

### Change Items Per Page

Edit `invoice_template.html`:
```jinja2
{% set items_per_page = 5 %}  {# Default is 3 #}
```

### Modify PDF Conversion Settings

Edit `pdf_converter.py` to customize WeasyPrint options:

```python
HTML(string=html_content, base_url=base_url).write_pdf(
    pdf_path,
    stylesheets=None,  # Add custom CSS
    presentational_hints=True,
    optimize_images=True  # Reduce file size
)
```

## 📊 Performance

### Typical Generation Times

| Operation | Time |
|-----------|------|
| HTML Generation | < 1 second |
| PDF Generation (Docker) | 3-5 seconds |
| - First run | ~5 seconds |
| - Subsequent runs | ~3 seconds |
| Total (HTML + PDF) | 4-6 seconds |

### Performance Tips

1. **Batch Processing**: Generate multiple PDFs in sequence to amortize Docker startup
2. **Keep Docker Running**: Don't stop Docker Desktop during operation
3. **Optimize Images**: Use compressed logo images
4. **Reuse Connections**: Use same output directory for multiple invoices

## 🔄 Updating

### Update Docker Image

After modifying `Dockerfile` or `pdf_converter.py`:

```bash
# Rebuild image
docker build -t invoice-pdf-generator .

# Or force rebuild (no cache)
docker build --no-cache -t invoice-pdf-generator .
```

### Update Python Code

After modifying `generate_invoice.py`:
```bash
# No rebuild needed - just run the updated script
python generate_invoice.py
```

## 🧹 Cleanup

### Remove Docker Image

```bash
docker rmi invoice-pdf-generator
```

### Remove All Unused Docker Resources

```bash
docker system prune -a
```

**Warning**: This removes ALL unused Docker images, not just this one.

## 📝 Complete Example Workflow

```python
#!/usr/bin/env python3
"""
Complete invoice generation workflow
"""

from generate_invoice import generate_invoice_html
import json
from pathlib import Path

# 1. Prepare data
invoice_data = {
    "logo_path": "company_logo.jpeg",
    "carrox_logo_path": "carrox_logo.png",
    "supplier": {
        "name": "My Company Ltd",
        "address_line1": "123 Business Street",
        "address_line2": "Dublin D01, Ireland",
        "email": "info@mycompany.ie",
        "phone": "+353 1 234 5678",
        "vat_no": "IE1234567XX",
        "vrt_tan": "VRT123"
    },
    "invoice": {
        "number": "INV-2025-001",
        "ref_po": "PO-12345",
        "date": "31/01/2025"
    },
    # ... rest of data
    "items": [
        # ... vehicle items
    ]
}

# 2. Save data to JSON file (optional)
output_dir = Path("invoices")
output_dir.mkdir(exist_ok=True)

json_path = output_dir / "invoice_data.json"
with open(json_path, 'w') as f:
    json.dump(invoice_data, f, indent=2)

# 3. Generate HTML and PDF
generate_invoice_html(
    json_data=invoice_data,  # Or use json_path
    template_path='invoice_template.html',
    output_path=output_dir / 'INV-2025-001.html',
    generate_pdf=True
)

print("\n✓ Invoice generation complete!")
print(f"  HTML: {output_dir}/INV-2025-001.html")
print(f"  PDF:  {output_dir}/INV-2025-001.pdf")
```

## 🔐 Security Notes

1. **Volume Mounting**: Only mount directories you trust
2. **Image Source**: Always build from your own Dockerfile
3. **Data Privacy**: All processing is local - no data sent to cloud
4. **File Permissions**: Container runs with standard user permissions

## 📚 Additional Resources

- **WeasyPrint Documentation**: https://weasyprint.org/
- **Docker Documentation**: https://docs.docker.com/
- **Jinja2 Template Guide**: https://jinja.palletsprojects.com/

## ✅ Deployment Checklist

- [ ] Docker Desktop installed and running
- [ ] Docker image built: `docker images invoice-pdf-generator`
- [ ] Test conversion: Generate sample invoice
- [ ] Verify logos appear in PDF
- [ ] Test with various item counts
- [ ] Verify page breaks are correct
- [ ] Set up error handling
- [ ] Document for your team
- [ ] Test on target deployment environment

## 💡 Tips & Best Practices

1. **Build Once**: Docker image only needs to be built once
2. **Test with HTML First**: Debug layout issues in HTML before generating PDF
3. **Logo Placement**: Keep logos in same directory as output for reliability
4. **Batch Operations**: Process multiple invoices together for efficiency
5. **Error Handling**: Always check return value of `convert_html_to_pdf()`
6. **File Naming**: Use invoice numbers in filenames for easy organization
7. **Archival**: PDFs are better for long-term storage than HTML

## 🆘 Getting Help

If you encounter issues:

1. Check Docker is running: `docker info`
2. Verify image exists: `docker images invoice-pdf-generator`
3. Test HTML generation first (without PDF)
4. Check file paths are absolute
5. Verify logo files exist
6. Review Docker logs: `docker logs <container-id>`

## 📖 Quick Reference

### Build Docker Image
```bash
docker build -t invoice-pdf-generator .
```

### Generate Invoice (Python)
```python
from generate_invoice import generate_invoice_html
generate_invoice_html('data.json', generate_pdf=True)
```

### Convert HTML to PDF (Python)
```python
from generate_invoice import convert_html_to_pdf
convert_html_to_pdf('invoice.html', 'invoice.pdf')
```

### Manual Docker Conversion
```bash
docker run --rm -v "$(pwd):/data" invoice-pdf-generator /data/input.html /data/output.pdf
```
