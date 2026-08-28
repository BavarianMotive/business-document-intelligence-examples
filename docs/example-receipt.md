# Synthetic receipt to JSON example

This example shows the shape of a receipt extraction response from **Business Document Intelligence** using a synthetic receipt. The values are illustrative and do not represent a real customer transaction.

## Example receipt

```text
EXAMPLE MARKET
100 Main Street
Boston, MA 02110

Receipt R-1042
2026-08-28 14:35

2 x Sparkling Water @ $3.00    $6.00
1 x Sandwich                  $12.00
1 x Fruit                      $2.00

Subtotal                      $20.00
Tax                            $1.60
Tip                            $2.00
Discount                       $1.00
Total                          $22.60

Visa **** 4242
```

## Representative JSON

```json
{
  "data": {
    "document_type": "receipt",
    "merchant": {
      "name": "EXAMPLE MARKET",
      "address": "100 Main Street, Boston, MA 02110",
      "tax_id": null,
      "phone": null
    },
    "receipt_number": "R-1042",
    "transaction_date": "2026-08-28",
    "transaction_time": "14:35",
    "currency": "USD",
    "payment_method": "Visa",
    "payment_card_last4": "4242",
    "subtotal": 20.0,
    "tax": 1.6,
    "tip": 2.0,
    "discount": 1.0,
    "total": 22.6,
    "line_items": [
      {
        "description": "Sparkling Water",
        "sku": null,
        "quantity": 2,
        "unit_price": 3.0,
        "amount": 6.0
      },
      {
        "description": "Sandwich",
        "sku": null,
        "quantity": 1,
        "unit_price": 12.0,
        "amount": 12.0
      },
      {
        "description": "Fruit",
        "sku": null,
        "quantity": 1,
        "unit_price": 2.0,
        "amount": 2.0
      }
    ],
    "notes": null
  },
  "validation": {
    "core_fields_complete": true,
    "missing_core_fields": [],
    "totals_reconciled": true,
    "line_items_reconciled": true,
    "warnings": []
  },
  "meta": {
    "schema_version": "receipt.v1",
    "api_version": "0.6.0"
  }
}
```

The API keeps missing or ambiguous values as `null` rather than inventing them. Receipt responses expose at most the last four payment-card digits.

For a complete Python walkthrough, see **[Receipt OCR API: Convert Receipt Images to Structured JSON with Python](tutorial-python-receipt-to-json.md)**.
