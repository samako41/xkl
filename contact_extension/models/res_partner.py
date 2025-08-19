from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    payment_hold_status = fields.Boolean(
        string="Payment Hold Status",
        help="1 = On Hold, 0 = Not on Hold"
    )

    payment_priority = fields.Integer(
        string="Payment Priority",
        help="1 - 99 (lower = higher priority)"
    )

    # bank_code = fields.Char(
    #     string="Bank Code"
    # )
    fax = fields.Char(
        string="Fax"
    )

    ap_distribution_acct = fields.Char(
        string="AP Distribution Acct."
    )

    vendor_note_code = fields.Char(
        string="Vendor's Note Code"
    )

    # credit_limit_vendor = fields.Float(
    #     string="Credit Limit with Vendor"
    # )

    vendor_inactive_flag = fields.Selection(
        [
            ('1', 'Active'),
            ('0', 'Inactive'),
        ],
        string="Vendor Inactive Flag",
        default='1',
        help="1 = Active, 0 = Inactive"
    )

    ar_resale_number = fields.Char(
        string="AR Resale Number"
    )

    ar_hold_status = fields.Boolean(
        string="AR Hold Status",
        help="1 = On Hold, 0 = Not on Hold"
    )

    freight_terms_code = fields.Char(
        string="Freight Terms Code"
    )

    monthly_finance_charge = fields.Float(
        string="Monthly Finance Charge (%)"
    )

    credit_review_date = fields.Date(
        string="Credit Review Date"
    )

    standard_discount_percent = fields.Float(
        string="Standard Discount (%)"
    )

    arfax = fields.Char(
        string="Fax"
    )

    ups_fedex_number = fields.Char(
        string="UPS/FedEx #"
    )

    bill_freight = fields.Selection(
        [
            ('P', 'Prepaid'),
            ('A', 'Prepaid & Add'),
            ('R', 'Recipient'),
            ('T', 'Third Party'),
            ('C', 'Consignee')
        ],
        string="Bill Freight"
    )

    tax_code = fields.Char(
        string="Tax Code"
    )
