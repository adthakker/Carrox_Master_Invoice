# Invoice JSON Schema Reference

Quick reference for all fields in the invoice JSON data structure.

## Required Fields

### Logo Paths
```json
"logo_path": "string - path to company logo image",
"carrox_logo_path": "string - path to CarRox logo image"
```

### Supplier (all fields required)
```json
"supplier": {
  "name": "string",
  "address_line1": "string",
  "address_line2": "string",
  "email": "string (email format)",
  "phone": "string",
  "vat_no": "string",
  "vrt_tan": "string"
}
```

### Invoice (all fields required)
```json
"invoice": {
  "number": "string - invoice number",
  "ref_po": "string - PO reference",
  "date": "string - date in dd/mm/yyyy format"
}
```

### Customer (all fields required)
```json
"customer": {
  "name": "string",
  "address": "string",
  "email": "string (email format)"
}
```

### Shipping (all fields required)
```json
"shipping": {
  "due_date": "string - dd/mm/yyyy",
  "items_count": "string - e.g., '77 Used Cars'",
  "from_to": "string - sender name",
  "shipped_via": "string - shipping method",
  "irl_eta": "string - dd/mm/yyyy",
  "irl_delivery": "string - delivery note"
}
```

### Payment (all fields required)
```json
"payment": {
  "bank_name": "string",
  "bank_address": "string",
  "iban": "string",
  "in_favor_of": "string - account holder",
  "phone": "string"
}
```

### Summary (all fields required, pre-formatted with currency)
```json
"summary": {
  "total_cif": "string - e.g., '€694,021.85'",
  "yen_equivalent": "string - e.g., '¥121,722,272'",
  "fx_rate": "string - e.g., '175.3868'",
  "cct": "string - e.g., '€23,772.60'",
  "clearance": "string - e.g., '€4,620.00'",
  "port_handling": "string - e.g., '€6,295.00'",
  "devanning": "string - e.g., '€16,680.00'",
  "broker_fees": "string - e.g., '€39,715.00'",
  "total_excluding_vat": "string - e.g., '€785,104.45'",
  "vat_23": "string - e.g., '€178,072.77'",
  "total_fully_delivered": "string - e.g., '€963,177.23'"
}
```

### Balance (all fields required, pre-formatted with currency)
```json
"balance": {
  "total_cif_77_cars": "string - e.g., '¥121,722,272'",
  "order_deposit": "string - e.g., '¥8,538,192'",
  "yen_fx_forward": "string - e.g., '¥113,184,080'",
  "due_euro_equivalent": "string - e.g., '€644,720.01'",
  "fx_forward_rate": "string - e.g., '175.5554'",
  "due_import_costs": "string - e.g., '€269,155.37'",
  "total_balance_due": "string - e.g., '€913,875.39'",
  "paid_to_date": "string - e.g., '€447,642.38'",
  "paid_date": "string - dd/mm/yyyy",
  "remaining_due": "string - e.g., '€466,233.01'"
}
```

### Items (array of objects)
```json
"items": [
  {
    "make": "string - e.g., 'TOYOTA'",
    "model_code": "string - e.g., 'DAA-ZYX10'",
    "model": "string - e.g., 'C-HR HYBRID'",
    "year": "string - e.g., '2017'",
    "color": "string - e.g., 'silver'",
    "month": "string - e.g., '4'",
    "chassis_no": "string - chassis number",
    "engine_no": "string - engine number (can be empty '')",
    "car_cost": "string - e.g., '¥1,250,000' (can be empty '')",
    "odometer": "string - e.g., '8888'",
    "insurance": "string - e.g., '¥5,000'",
    "freight": "string - e.g., '¥179,936'",
    "total_cif_yen": "string - e.g., '¥1,438,036'",
    "cif_euro": "string - e.g., '€8,199.23'",
    "cct": "string - e.g., '€106.59'",
    "clearance": "string - e.g., '€60.00'",
    "port_handling": "string - e.g., '€88.00'",
    "devanning": "string - e.g., '€300.00'",
    "broker_fees": "string - e.g., '€495.00'",
    "vat": "string - e.g., '€2,093.19'",
    "total": "string - e.g., '€11,342.00'",
    "delivery_location": "string - e.g., '[Delivery location]'"
  }
]
```

### Pagination (optional - auto-calculated if omitted)
```json
"pagination": {
  "current_page": 1,
  "total_pages": 14
}
```

## Field Notes

### Optional/Empty Fields
- `engine_no` - can be empty string `""`
- `car_cost` - can be empty string `""`
- `pagination.total_pages` - if omitted, auto-calculated as: 1 + ceil(items_count / 3)

### Formatting Guidelines

#### Currency Values
Always include currency symbol and proper formatting:
- ✅ Correct: `"€694,021.85"`, `"¥121,722,272"`
- ❌ Incorrect: `694021.85`, `"694021.85"`, `121722272`

#### Dates
Always use dd/mm/yyyy format:
- ✅ Correct: `"23/12/2025"`
- ❌ Incorrect: `"2025-12-23"`, `"12/23/2025"`

#### Numeric Strings
Year, month, odometer should be strings:
- ✅ Correct: `"2017"`, `"4"`, `"8888"`
- ❌ Incorrect: `2017`, `4`, `8888`

## Validation Checklist

Before generating invoice, verify:

- [ ] All image paths exist and are accessible
- [ ] All required sections present (supplier, invoice, customer, shipping, payment, summary, balance)
- [ ] All currency values include symbols (€ or ¥)
- [ ] All dates in dd/mm/yyyy format
- [ ] Items array has at least 1 item
- [ ] Each item has all required fields
- [ ] Email addresses are valid format
- [ ] No missing fields (can be empty strings, but must be present)

## Python Data Type Example

```python
invoice_data = {
    "logo_path": str,
    "carrox_logo_path": str,
    "supplier": {
        "name": str,
        "address_line1": str,
        "address_line2": str,
        "email": str,
        "phone": str,
        "vat_no": str,
        "vrt_tan": str
    },
    "invoice": {
        "number": str,
        "ref_po": str,
        "date": str  # "dd/mm/yyyy"
    },
    "customer": {
        "name": str,
        "address": str,
        "email": str
    },
    "shipping": {
        "due_date": str,  # "dd/mm/yyyy"
        "items_count": str,
        "from_to": str,
        "shipped_via": str,
        "irl_eta": str,  # "dd/mm/yyyy"
        "irl_delivery": str
    },
    "payment": {
        "bank_name": str,
        "bank_address": str,
        "iban": str,
        "in_favor_of": str,
        "phone": str
    },
    "summary": {
        "total_cif": str,  # "€694,021.85"
        "yen_equivalent": str,  # "¥121,722,272"
        "fx_rate": str,  # "175.3868"
        "cct": str,
        "clearance": str,
        "port_handling": str,
        "devanning": str,
        "broker_fees": str,
        "total_excluding_vat": str,
        "vat_23": str,
        "total_fully_delivered": str
    },
    "balance": {
        "total_cif_77_cars": str,
        "order_deposit": str,
        "yen_fx_forward": str,
        "due_euro_equivalent": str,
        "fx_forward_rate": str,
        "due_import_costs": str,
        "total_balance_due": str,
        "paid_to_date": str,
        "paid_date": str,  # "dd/mm/yyyy"
        "remaining_due": str
    },
    "items": [
        {
            "make": str,
            "model_code": str,
            "model": str,
            "year": str,
            "color": str,
            "month": str,
            "chassis_no": str,
            "engine_no": str,  # can be ""
            "car_cost": str,  # can be ""
            "odometer": str,
            "insurance": str,
            "freight": str,
            "total_cif_yen": str,
            "cif_euro": str,
            "cct": str,
            "clearance": str,
            "port_handling": str,
            "devanning": str,
            "broker_fees": str,
            "vat": str,
            "total": str,
            "delivery_location": str
        }
    ],
    "pagination": {
        "current_page": int,  # typically 1
        "total_pages": int  # optional, auto-calculated if omitted
    }
}
```
