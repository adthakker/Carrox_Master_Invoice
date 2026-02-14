import pandas as pd
import json
import os
from datetime import datetime

# Define structure for the template
TEMPLATE_STRUCTURE = {
    "Details": {
        "Fields": [
            "Supplier Name", "Supplier Address 1", "Supplier Address 2", "Supplier Email", "Supplier Phone", "Supplier VAT", "Supplier VRT TAN",
            "Invoice Number", "Ref PO", "Invoice Date",
            "Customer Name", "Customer Address", "Customer Email",
            "Shipping Due Date", "Items Count", "From/To", "Shipped Via", "IRL ETA", "IRL Delivery",
            "Bank Name", "Bank Address", "IBAN", "Account Name", "Bank Phone",
            "Total CIF", "Yen Equivalent", "FX Rate", "CCT", "Clearance", "Port Handling", "Devanning", "Broker Fees", "Total Excl VAT", "VAT 23%", "Total Fully Delivered",
            "Balance Total CIF", "Order Deposit", "Yen FX Forward", "Due Euro Equivalent", "FX Forward Rate", "Due Import Costs", "Total Balance Due", "Paid To Date", "Paid Date", "Remaining Due"
        ],
        "Values": [
            "My Company Ltd", "123 Business St", "Dublin, Ireland", "info@company.com", "+353 1 234 5678", "IE1234567XX", "VRT123",
            "INV-001", "PO-001", "31/01/2025",
            "Customer Name", "Customer Address", "customer@email.com",
            "28/02/2025", "5 Cars", "Japan to Dublin", "MSC", "15/03/2025", "Delivery Note",
            "Bank of Ireland", "Dublin Branch", "IE89BOFI900000000", "Company Account", "+353 1 670 0000",
            "€100,000.00", "¥14,000,000", "140.00", "€1,000.00", "€100.00", "€150.00", "€300.00", "€500.00", "€102,050.00", "€23,471.50", "€125,521.50",
            "¥14,000,000", "¥1,000,000", "¥13,000,000", "€92,857.14", "140.00", "€32,664.36", "€125,521.50", "€50,000.00", "30/01/2025", "€75,521.50"
        ]
    },
    "Items": {
        "Columns": [
            "Make", "Model Code", "Model", "Year", "Color", "Month", 
            "Chassis No", "Engine No", "Car Cost", "Odometer", 
            "Insurance", "Freight", "Total CIF Yen", "CIF Euro",
            "CCT", "Clearance", "Port Handling", "Devanning", 
            "Broker Fees", "VAT", "Total Euro", "Delivery Location", "Origin Statement"
        ],
        "Sample": [
            "TOYOTA", "DAA-ZYX10", "C-HR", "2020", "Silver", "4",
            "ZYX10-123456", "2ZR-12345", "¥1,500,000", "50000",
            "¥5,000", "¥100,000", "¥1,605,000", "€11,464.29",
            "€1,146.43", "€100.00", "€150.00", "€300.00",
            "€500.00", "€2,636.79", "€16,297.51", "[Delivery Location]", "The product is of Japanese Preferential Origin. [ COUNTRY OF ORIGIN JAPAN ]"
        ]
    }
}

def generate_template(output_path="invoice_data.xlsx"):
    """Generates an Excel template for invoice data."""
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Details (Transposed for easier entry)
            df_details = pd.DataFrame({
                "Field": TEMPLATE_STRUCTURE["Details"]["Fields"],
                "Value": TEMPLATE_STRUCTURE["Details"]["Values"]
            })
            df_details.to_excel(writer, sheet_name="Details", index=False)

            # Sheet 2: Items
            df_items = pd.DataFrame(
                [TEMPLATE_STRUCTURE["Items"]["Sample"]],
                columns=TEMPLATE_STRUCTURE["Items"]["Columns"]
            )
            df_items.to_excel(writer, sheet_name="Items", index=False)
            
        print(f"✓ Template generated: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error generating template: {e}")
        return False

def parse_excel(file_path):
    """Reads Excel file and returns JSON-compatible dictionary."""
    try:
        # Read Details Sheet
        df_details = pd.read_excel(file_path, sheet_name="Details")
        # Convert 2-column format (Field, Value) to dictionary
        details_dict = dict(zip(df_details["Field"], df_details["Value"]))
        
        # Read Items Sheet
        df_items = pd.read_excel(file_path, sheet_name="Items")
        items_list = df_items.to_dict(orient="records")
        
        # Helper to safely get value or empty string
        def get_val(key):
            val = details_dict.get(key, "")
            return format_if_numeric(val, key)

        def format_if_numeric(val, key=""):
            """Formats numeric values as currency strings based on key or content."""
            if pd.isna(val) or val == "":
                return ""
            
            # If it's already a string with currency symbol, return as is
            s_val = str(val).strip()
            if any(symbol in s_val for symbol in ['€', '¥', '$', '£']):
                return s_val
                
            # Try to parse as float
            try:
                # Remove common non-numeric chars except dot/comma before parsing if needed? 
                # Pandas usually gives us float/int if it's a number.
                num_val = float(val)
                
                # Determine currency based on key context
                key_lower = key.lower()
                
                # YEN fields
                if "yen" in key_lower or "car_cost" in key_lower or "freight" in key_lower or "insurance" in key_lower:
                    # Yen usually has no decimals
                    return f"¥{int(num_val):,}"
                
                # EURO fields (default for others in this context)
                # Includes: cif_euro, cct, clearance, handling, devanning, fees, vat, total
                else:
                    return f"€{num_val:,.2f}"
            except (ValueError, TypeError):
                # Not a number, return original string
                return s_val


        # Construct JSON logical structure
        invoice_data = {
            "logo_path": "company_logo.jpeg", # Defaults
            "carrox_logo_path": "carrox_logo.png",
            
            "supplier": {
                "name": get_val("Supplier Name"),
                "address_line1": get_val("Supplier Address 1"),
                "address_line2": get_val("Supplier Address 2"),
                "email": get_val("Supplier Email"),
                "phone": get_val("Supplier Phone"),
                "vat_no": get_val("Supplier VAT"),
                "vrt_tan": get_val("Supplier VRT TAN")
            },
            "invoice": {
                "number": get_val("Invoice Number"),
                "ref_po": get_val("Ref PO"),
                "date": get_val("Invoice Date")
            },
            "customer": {
                "name": get_val("Customer Name"),
                "address": get_val("Customer Address"),
                "email": get_val("Customer Email")
            },
            "shipping": {
                "due_date": get_val("Shipping Due Date"),
                "items_count": get_val("Items Count"),
                "from_to": get_val("From/To"),
                "shipped_via": get_val("Shipped Via"),
                "irl_eta": get_val("IRL ETA"),
                "irl_delivery": get_val("IRL Delivery")
            },
            "payment": {
                "bank_name": get_val("Bank Name"),
                "bank_address": get_val("Bank Address"),
                "iban": get_val("IBAN"),
                "in_favor_of": get_val("Account Name"),
                "phone": get_val("Bank Phone")
            },
            "summary": {
                "total_cif": get_val("Total CIF"),
                "yen_equivalent": get_val("Yen Equivalent"),
                "fx_rate": get_val("FX Rate"),
                "cct": get_val("CCT"),
                "clearance": get_val("Clearance"),
                "port_handling": get_val("Port Handling"),
                "devanning": get_val("Devanning"),
                "broker_fees": get_val("Broker Fees"),
                "total_excluding_vat": get_val("Total Excl VAT"),
                "vat_23": get_val("VAT 23%"),
                "total_fully_delivered": get_val("Total Fully Delivered")
            },
            "balance": {
                "total_cif_77_cars": get_val("Balance Total CIF"),
                "order_deposit": get_val("Order Deposit"),
                "yen_fx_forward": get_val("Yen FX Forward"),
                "due_euro_equivalent": get_val("Due Euro Equivalent"),
                "fx_forward_rate": get_val("FX Forward Rate"),
                "due_import_costs": get_val("Due Import Costs"),
                "total_balance_due": get_val("Total Balance Due"),
                "paid_to_date": get_val("Paid To Date"),
                "paid_date": get_val("Paid Date"),
                "remaining_due": get_val("Remaining Due")
            },
            "items": []
        }

        # Process Items
        for item in items_list:
            # Handle potential NaN values in items
            clean_item = {
                "make": str(item.get("Make", "")),
                "model_code": str(item.get("Model Code", "")),
                "model": str(item.get("Model", "")),
                "year": str(item.get("Year", "")),
                "color": str(item.get("Color", "")),
                "month": str(item.get("Month", "")),
                "chassis_no": str(item.get("Chassis No", "")),
                "engine_no": str(item.get("Engine No", "") or ""),
                
                # Format currency fields
                "car_cost": format_if_numeric(item.get("Car Cost", ""), "car_cost"),
                "odometer": str(item.get("Odometer", "")), # Not currency
                "insurance": format_if_numeric(item.get("Insurance", ""), "insurance"),
                "freight": format_if_numeric(item.get("Freight", ""), "freight"),
                "total_cif_yen": format_if_numeric(item.get("Total CIF Yen", ""), "total_cif_yen"),
                
                "cif_euro": format_if_numeric(item.get("CIF Euro", ""), "cif_euro"),
                "cct": format_if_numeric(item.get("CCT", ""), "cct"),
                "clearance": format_if_numeric(item.get("Clearance", ""), "clearance"),
                "port_handling": format_if_numeric(item.get("Port Handling", ""), "port_handling"),
                "devanning": format_if_numeric(item.get("Devanning", ""), "devanning"),
                "broker_fees": format_if_numeric(item.get("Broker Fees", ""), "broker_fees"),
                "vat": format_if_numeric(item.get("VAT", ""), "vat"),
                "total": format_if_numeric(item.get("Total Euro", ""), "total"),
                
                "delivery_location": str(item.get("Delivery Location", "")),
                "origin_text": str(item.get("Origin Statement", ""))
            }
            # Remove keys with value "nan" string if any crept in
            clean_item = {k: v if v.lower() != 'nan' else '' for k, v in clean_item.items()}
            invoice_data["items"].append(clean_item)

        return invoice_data

    except Exception as e:
        print(f"Error parsing Excel: {e}")
        return None

if __name__ == "__main__":
    generate_template()
