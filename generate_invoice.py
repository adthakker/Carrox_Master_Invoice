#!/usr/bin/env python3
"""
Invoice Generator using Jinja2 Template with Docker PDF Support
Generates HTML invoices from JSON data and converts to PDF using Docker
Final Complete Version
"""

import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import subprocess
from pathlib import Path
import argparse
import sys
try:
    import excel_utils
except ImportError:
    excel_utils = None


def load_invoice_data(json_file_path):
    """
    Load invoice data from JSON file
    
    Args:
        json_file_path (str): Path to JSON file containing invoice data
        
    Returns:
        dict: Invoice data
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)





def convert_html_to_pdf(html_path, pdf_path=None, docker_image='carrox-invoice-pdf-generator'):
    """
    Convert HTML to PDF using Docker container with WeasyPrint
    
    Args:
        html_path (str): Path to HTML file
        pdf_path (str): Path for PDF output (default: same as HTML with .pdf extension)
        docker_image (str): Docker image name (default: 'carrox-invoice-pdf-generator')
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Set default PDF path
    if pdf_path is None:
        pdf_path = str(Path(html_path).with_suffix('.pdf'))
    
    # Convert to absolute paths
    html_path = os.path.abspath(html_path)
    pdf_path = os.path.abspath(pdf_path)
    
    # Get directory and filenames
    work_dir = os.path.dirname(html_path)
    html_filename = os.path.basename(html_path)
    pdf_filename = os.path.basename(pdf_path)
    
    print(f"\n Converting HTML to PDF using Docker...")
    print(f"  Image: {docker_image}")
    print(f"  HTML:  {html_path}")
    print(f"  PDF:   {pdf_path}")
    
    try:
        # Check if Docker is available
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Error: Docker is not installed or not running")
        print("  Please install Docker Desktop: https://www.docker.com/products/docker-desktop")
        return False
    
    try:
        # Check if image exists
        check_result = subprocess.run(
            ['docker', 'images', '-q', docker_image],
            capture_output=True,
            text=True
        )
        
        if not check_result.stdout.strip():
            print(f"✗ Error: Docker image '{docker_image}' not found")
            print(f"  Please build the image first:")
            print(f"  docker build -t {docker_image} .")
            return False
        
        # Run Docker container to convert HTML to PDF
        docker_cmd = [
            'docker', 'run', '--rm',
            '-v', f'{work_dir}:/data',
            docker_image,
            f'/data/{html_filename}',
            f'/data/{pdf_filename}'
        ]
        
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        # Check success
        if result.returncode == 0 and os.path.exists(pdf_path):
            return True
        else:
            print(f"✗ PDF generation failed (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Error: PDF generation timed out")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def generate_invoice_html(json_data, template_path='invoice_template.html', output_path='generated_invoice.html', generate_pdf=False):
    """
    Generate HTML invoice from JSON data using Jinja2 template
    
    Args:
        json_data (dict or str): Invoice data as dictionary or path to JSON file
        template_path (str): Path to Jinja2 template file
        output_path (str): Path where generated HTML will be saved
        generate_pdf (bool): If True, also generate PDF using Docker (default: False)
        
    Returns:
        str: Generated HTML content
    """
    # Load JSON data if path is provided
    if isinstance(json_data, str):
        json_data = load_invoice_data(json_data)
    
    # Calculate pagination if not provided
    # Remove manual pagination calculation
    if 'pagination' not in json_data:
        json_data['pagination'] = {}
    
    # We let WeasyPrint handle total pages via CSS vars, but we can set a dummy value if needed
    # or just remove references to total_pages in the template that assume manual calc.
    # For now, we'll keep the object to avoid key errors but it won't be used for loop control.
    json_data['pagination']['current_page'] = 1
    json_data['pagination']['total_pages'] = 1  # Placeholder, not used in new native pagination

    
    # Setup Jinja2 environment
    template_dir = os.path.dirname(os.path.abspath(template_path))
    template_name = os.path.basename(template_path)
    
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Load template
    template = env.get_template(template_name)
    
    # Render template with data
    html_content = template.render(**json_data)
    
    # Save to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f" Invoice generated successfully: {output_path}")
    print(f"  - Total items: {len(json_data.get('items', []))}")
    print(f"  - Total pages: {json_data['pagination']['total_pages']}")
    
    # Generate PDF if requested
    if generate_pdf:
        pdf_path = str(Path(output_path).with_suffix('.pdf'))
        success = convert_html_to_pdf(output_path, pdf_path)
        if success:
            print(f"PDF generated: {pdf_path}")
        else:
            print(f"  PDF generation failed. HTML is still available at: {output_path}")
    
    return html_content


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Generate Invoice HTML and PDF')
    parser.add_argument('--excel', help='Path to Excel input file (mutually exclusive with JSON)')
    parser.add_argument('--json', help='Path to JSON input file')
    parser.add_argument('input_file', nargs='?', help='Legacy position argument (JSON file)')
    
    args = parser.parse_args()
    
    # Determine input file
    json_file = None
    excel_file = None
    
    if args.excel:
        excel_file = args.excel
    elif args.json:
        json_file = args.json
    elif args.input_file:
        # Check extension to decide
        if args.input_file.lower().endswith(('.xlsx', '.xls')):
            excel_file = args.input_file
        else:
            json_file = args.input_file
    else:
        # Default behavior
        script_dir = Path(__file__).parent.resolve()
        json_file = script_dir / 'sample_invoice_data.json'
        print(f"No input specified, using default: {json_file}")
        if not json_file.exists():
             # Fallback to checking for excel default
            default_excel = script_dir / 'invoice_data.xlsx'
            if default_excel.exists():
                print(f"Default JSON not found, found Excel: {default_excel}")
                excel_file = str(default_excel)
                json_file = None

    # Process Input
    final_json_path = json_file
    
    if excel_file:
        if not excel_utils:
            print("Error: excel_utils module not found. Cannot process Excel files.")
            sys.exit(1)
            
        print(f"Processing Excel file: {excel_file}")
        data = excel_utils.parse_excel(excel_file)
        if not data:
            print("Failed to parse Excel file.")
            sys.exit(1)
            
        # Save debug JSON
        debug_json_path = 'debug_derived_data.json'
        with open(debug_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Debug JSON saved to: {debug_json_path}")
        
        final_json_path = debug_json_path

    if not final_json_path or not os.path.exists(final_json_path):
        print(f"Error: Input file not found: {final_json_path}")
        sys.exit(1)

    print(f"Generating invoice from {final_json_path}...")
    print(f"=" * 60)
    
    # Generate HTML and PDF
    output_base = os.path.splitext(os.path.basename(final_json_path))[0]
    if output_base == 'debug_derived_data':
        output_base = 'invoice_from_excel'
        
    generate_invoice_html(
        json_data=str(final_json_path),
        output_path=f'{output_base}.html',
        generate_pdf=True
    )
    
    print(f"\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
