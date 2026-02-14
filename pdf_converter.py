#!/usr/bin/env python3
"""
PDF Converter using WeasyPrint
Runs inside Docker container to convert HTML to PDF
Final Version
"""

import sys
import os
from pathlib import Path
from weasyprint import HTML


def convert_html_to_pdf(html_path, pdf_path):
    """
    Convert HTML file to PDF using WeasyPrint
    
    Args:
        html_path (str): Path to input HTML file
        pdf_path (str): Path to output PDF file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"[WeasyPrint] Converting HTML to PDF...")
        print(f"[WeasyPrint]   Input:  {html_path}")
        print(f"[WeasyPrint]   Output: {pdf_path}")
        
        # Check if input file exists
        if not os.path.exists(html_path):
            print(f"[WeasyPrint] Error: Input file not found: {html_path}")
            return False
        
        # Get base URL for resolving relative paths (for images/CSS)
        base_url = Path(html_path).parent.as_uri() + '/'
        print(f"[WeasyPrint]   Base URL: {base_url}")
        
        # Read HTML content
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert to PDF
        HTML(string=html_content, base_url=base_url).write_pdf(pdf_path)
        
        # Verify PDF was created
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"[WeasyPrint] ✓ PDF generated successfully!")
            print(f"[WeasyPrint]   Size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
            return True
        else:
            print(f"[WeasyPrint] Error: PDF file was not created")
            return False
            
    except Exception as e:
        print(f"[WeasyPrint] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python pdf_converter.py <input.html> <output.pdf>")
        print("")
        print("Example:")
        print("  python pdf_converter.py /data/invoice.html /data/invoice.pdf")
        sys.exit(1)
    
    html_path = sys.argv[1]
    pdf_path = sys.argv[2]
    
    # Create output directory if needed
    output_dir = os.path.dirname(pdf_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Convert
    success = convert_html_to_pdf(html_path, pdf_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
