# XKL Sale Quote PDF Report — Odoo 18 Module

## Overview

This module extends the **Sale Order** in Odoo 18 to generate a full
**XKL-branded multi-page proposal PDF**, matching the layout of the
Glasgow EPB proposal document.

---

## What it adds

### Button on the Sale Order form
A **"🖨 Print XKL Proposal"** button in the smart-button area of
every Sale Order opens the generated PDF directly.

The same report is also accessible via **Print → XKL Proposal** in
the Action menu.

### "XKL Proposal" tab on the Sale Order form
All proposal narrative fields are editable directly on the order,
grouped by PDF page:

| Section               | Page | Field type        |
|-----------------------|------|-------------------|
| Quote Meta            | 1    | Char / Date       |
| Introduction          | 2    | HTML (rich text)  |
| Strategic Objectives  | 2    | Text (plain)      |
| Conclusion            | 2    | HTML (rich text)  |
| XKL History           | 3    | HTML (rich text)  |
| Customer Requirements | 4    | Char (plain)      |
| Customised Solution   | 5    | HTML (rich text)  |
| Future Upgrades       | 6    | HTML (rich text)  |
| Sales Order Additions | 7    | HTML (rich text)  |

### "Included Components" column on order lines
Each sale order line gains an **Included Components** text field.
Content is split on newlines and rendered as bullet points under the
product name in the Page 7 sales order table.

---

## Generated PDF pages

| Page | Content |
|------|---------|
| 1 | Cover — client name, proposal title, date |
| 2 | Introduction · Strategic Objectives · Conclusion |
| 3 | XKL History, Customer Benefits, Testimonials |
| 4 | Customer Requirements table |
| 5 | Customised Solution description |
| 6 | Future Upgrades · System Highlight |
| 7 | Full Sales Order Form — line items, pricing, totals, cost per 100G |

---

## Installation

1. Copy the `xkl_sale_quote` folder into your Odoo 18 **addons** directory.
2. Restart the Odoo server:
   ```bash
   ./odoo-bin -c odoo.conf -d <your_db> -u xkl_sale_quote
   ```
   Or via the Odoo shell:
   ```bash
   ./odoo-bin shell -d <your_db>
   env['ir.module.module'].search([('name','=','xkl_sale_quote')]).button_immediate_install()
   ```
3. In **Settings → Apps**, search for **XKL Sale Quote PDF Report** and click **Install**.

---

## Dependencies

- `sale` (Sales module — standard Odoo 18)
- `mail` (for chatter on Sale Order)

No third-party Python packages required — PDF generation uses
Odoo's built-in **QWeb → wkhtmltopdf** pipeline.

---

## Configuration

All fields have sensible defaults pre-populated from the Glasgow EPB
proposal. Simply open any Sale Order, go to the **XKL Proposal** tab,
and edit the fields to match your engagement before printing.

---

## File Structure

```
xkl_sale_quote/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── sale_order.py          ← all new fields + button action
├── report/
│   ├── sale_quote_report.xml  ← ir.actions.report record
│   └── sale_quote_template.xml ← QWeb PDF template (7 pages)
├── security/
│   └── ir.model.access.csv
├── views/
│   └── sale_order_views.xml   ← button + XKL Proposal tab
└── README.md
```
