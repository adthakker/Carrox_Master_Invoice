# Dockerfile for Invoice PDF Generator using WeasyPrint
# Final Version - Compatible and Tested

FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies required by WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages with compatible versions
RUN pip install --no-cache-dir \
    weasyprint==60.2 \
    pydyf==0.10.0 \
    Pillow==10.2.0

# Copy the PDF converter script
COPY pdf_converter.py /app/

# Set permissions
RUN chmod +x /app/pdf_converter.py

# Entrypoint for direct execution
ENTRYPOINT ["python", "/app/pdf_converter.py"]
