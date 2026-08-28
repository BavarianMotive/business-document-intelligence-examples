# Synthetic invoice example

This example shows how a simple invoice maps into the normalized invoice schema. It is synthetic documentation, not an accuracy benchmark.

## Input

Imagine a PDF or image containing this invoice:

```text
Northwind Office Supply
Invoice INV-1042
Invoice date: 2026-08-15
Due date: 2026-09-14
PO: PO-818

Bill to: Example Company

2 x Office supplies @ $50.00
Subtotal: $100.00
Tax: $6.25
Total: $106.25
Amount due: $106.25
```

The actual API request sends the original PDF or image bytes, not this text representation.

## Normalized output shape

A corresponding invoice response can look like:

```json
{
  "data": {
    "document_type": "invoice",
    "vendor": {
      "name": "Northwind Office Supply"
    },
    "customer": {
      "name": "Example Company"
    },
    "invoice_number": "INV-1042",
    "purchase_order_number": "PO-818",
    "invoice_date": "2026-08-15",
    "due_date": "2026-09-14",
    "currency": "USD",
    "subtotal": 100.0,
    "tax": 6.25,
    "total": 106.25,
    "amount_due": 106.25,
    "line_items": [
      {
        "description": "Office supplies",
        "quantity": 2,
        "unit_price": 50.0,
        "amount": 100.0
      }
    ]
  },
  "validation": {
    "core_fields_complete": true,
    "missing_core_fields": [],
    "totals_reconciled": true,
    "line_items_reconciled": true,
    "warnings": []
  },
  "meta": {
    "schema_version": "invoice.v1",
    "api_version": "0.6.0"
  }
}
```

Real output depends on the source document. Missing or ambiguous fields may be returned as `null`.
