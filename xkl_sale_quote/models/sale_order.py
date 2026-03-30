# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ── Cover / Meta ──────────────────────────────────────────────────────────
    xkl_proposal_title = fields.Char(
        string='Proposal Title',
        default='Network Solution Proposal',
    )
    xkl_proposal_date = fields.Date(
        string='Proposal Date',
        default=fields.Date.today,
    )
    xkl_xkl_contact = fields.Char(
        string='XKL Contact',
        default='Casey Inman',
    )
    xkl_quote_number = fields.Char(
        string='Quote Number',
        compute='_compute_xkl_quote_number',
        store=True,
    )

    @api.depends('name')
    def _compute_xkl_quote_number(self):
        for rec in self:
            rec.xkl_quote_number = rec.name or ''

    # ── Page 2 — Introduction ─────────────────────────────────────────────────
    xkl_intro_body = fields.Html(
        string='Introduction Body',
        default="""<p>The Glasgow Electric Plant Board (GEPB), a municipal utility serving
Glasgow, Kentucky, has a long-standing commitment to providing reliable electric
and broadband services to its community. Building on this foundation, GEPB is
embarking on a long-haul dark fiber project to enhance regional connectivity,
improve network resilience, and support economic development in the area.
This initiative aims to address existing infrastructure challenges.</p>""",
    )

    # ── Page 2 — Strategic Objectives ────────────────────────────────────────
    xkl_objectives_intro = fields.Text(
        string='Objectives Intro',
        default=(
            'As the network expands, several operational and strategic initiatives '
            'necessitate investment in lighting long-haul dark fiber:'
        ),
    )
    xkl_objective_1 = fields.Text(
        string='Objective 1',
        default=(
            'High Cost of Leasing Backhaul Wavelengths – Third-party fiber lease '
            'agreements for middle-mile and long-haul connectivity introduce ongoing '
            'expenses, reducing profitability and control over network infrastructure.'
        ),
    )
    xkl_objective_2 = fields.Text(
        string='Objective 2',
        default=(
            'Limited Rural Connectivity – Businesses, municipalities, and internet '
            'service providers (ISPs) struggle with insufficient, unreliable, or '
            'expensive transport options in the region.'
        ),
    )
    xkl_objective_3 = fields.Text(
        string='Objective 3 (optional)',
    )

    # ── Page 2 — Conclusion ───────────────────────────────────────────────────
    xkl_conclusion_body = fields.Html(
        string='Conclusion Body',
        default="""<p>XKL can empower your organisation with <strong>license-free</strong>
optical networking solutions that will maximise Network backhaul and provide
resiliency. With <strong>no hidden fees, no licensing costs, and low operational
overhead</strong>, you can light dark fiber, expand bandwidth, and provide
reliable service to your community.</p>""",
    )

    # ── Page 3 — XKL History ──────────────────────────────────────────────────
    xkl_history_body = fields.Html(
        string='XKL History Body',
        default="""<p>For <strong>30+ years</strong>, XKL has been at the forefront of
fiber communications. Our rich history in R&amp;D allows us to help customers
solve their unique networking challenges with flexible and accessible DWDM solutions.
Created by CEO Len Bosack, co-founder of Cisco Systems, XKL brings decades of
expertise with a proven track record from 10G to 400G solutions, now advancing
towards 800G capabilities.</p>""",
    )
    xkl_warranty_highlight = fields.Char(
        string='Warranty Highlight',
        default='Up to 10-year warranty for all new products',
    )

    # ── Page 4 — Customer Requirements ───────────────────────────────────────
    xkl_req_sites = fields.Char(
        string='Sites',
        default='2 sites total: Glasgow and Bowling Green',
    )
    xkl_req_circuit = fields.Char(
        string='Circuit Specification',
        default='1 x 400G circuits between adjacent sites',
    )
    xkl_req_handoff = fields.Char(
        string='Client Handoff',
        default='100G client handoffs at each site',
    )
    xkl_req_otdr = fields.Char(
        string='OTDR Requirement',
        default='OTDR capability between each site',
    )
    xkl_req_distance = fields.Char(
        string='Link Distance',
        default='96 km',
    )
    xkl_req_extra = fields.Text(
        string='Additional Requirements (optional)',
    )

    # ── Page 5 — Customised Solution ─────────────────────────────────────────
    xkl_solution_body = fields.Html(
        string='Solution Description',
        default="""<p>This solution utilises a <strong>DQM400 Muxponder</strong> at each
site to provide 100G client handoffs and 400G line-side signals. Each DQM400 system
contains the 12-channel Mux/DeMux filters as well as the required EDFAs (Erbium
Doped Fiber Amplifiers).</p>
<p>Each client-side port in the DQM400 is populated with DR4+ transceivers.
Optionally, other 4×100G (DR4, PLR4, etc.) or 400G (FR4, LR4, etc.) transceivers
can be used. The interface encapsulation (4×100G versus 400G) is soft-configurable
and does <strong>not</strong> require any license fees.</p>""",
    )
    xkl_solution_link_distance = fields.Char(
        string='Supported Link Distance',
        default='116 km at 3 dBm power per channel (0.25 dB loss per km)',
    )
    xkl_solution_note = fields.Text(
        string='Technical Note',
        default=(
            'Final OTDR from the customer is required in order to confirm that the '
            'bill of materials in this proposal will satisfy the link budget of the '
            'actual customer fiber.'
        ),
    )

    # ── Page 6 — Future Upgrades ──────────────────────────────────────────────
    xkl_upgrade_body = fields.Html(
        string='Future Upgrades Body',
        default="""<p>Using the XKL Field Upgrade Package, additional 400G channels can
be installed into the DQM400. The system will then support a total of up to
<strong>16 × 100GE or 4 × 400GE</strong>, or a mix of 100GE and 400GE. For
further expansion, DQT400 Transponder systems can be added to support a total of
<strong>48 × 100GE or 12 × 400GE</strong>, or a mix of 100GE and 400GE.</p>""",
    )
    xkl_bert_note = fields.Text(
        string='BERT / System Highlight',
        default=(
            'XKL DarkStar systems are simple and easy to deploy. All systems can be '
            'configured in minutes with just a few commands. Fiber links can be tested '
            'using XKL\'s integrated Bit Error Ratio Test (BERT) feature to validate '
            'the data integrity of the fiber links.'
        ),
    )

    # ── Page 7 — Sales Order notes ────────────────────────────────────────────
    xkl_so_includes = fields.Html(
        string='Total Includes (printed on order)',
        default="""<ul>
  <li>$0 Licensing Fees for life of the product</li>
  <li><strong>Standard Warranty &amp; Customer Support – 1 year Included</strong>
    <ul>
      <li>Purchase covered under Standard Warranty from date of transfer to carrier</li>
      <li>24/7 phone access (support@xkl.com)</li>
      <li>Replacement or Repair of Defective Hardware</li>
    </ul>
  </li>
</ul>""",
    )
    xkl_so_notes = fields.Html(
        string='Order Notes (printed on order)',
        default="""<ol>
  <li>Quote is in US Dollars.</li>
  <li>Quote valid for 60 days.</li>
  <li>Payment terms are net 30 unless stated otherwise.</li>
  <li>Quote applies to this purchase only.</li>
  <li>Ships 8 weeks after acceptance of order.</li>
  <li>Financing options available upon request pursuant to completion of customer credit application.</li>
</ol>""",
    )

    # ── Computed helpers for the report ──────────────────────────────────────
    @api.depends('order_line.price_subtotal', 'order_line.price_total')
    def _compute_xkl_cost_per_100g(self):
        """
        Derive cost-per-100G circuit.
        Assumes each ordered unit carries 4 × 100G lanes.
        Falls back gracefully if qty is zero.
        """
        for rec in self:
            total_units = sum(rec.order_line.mapped('product_uom_qty'))
            circuits = total_units * 4  # 4 × 100G per muxponder
            if circuits:
                rec.xkl_cost_per_100g = rec.amount_total / circuits
            else:
                rec.xkl_cost_per_100g = 0.0

    xkl_cost_per_100g = fields.Float(
        string='Cost per 100G Circuit',
        compute='_compute_xkl_cost_per_100g',
        digits=(16, 2),
    )

    def action_print_xkl_proposal(self):
        """Button action — opens the PDF in a new tab."""
        return self.env.ref(
            'xkl_sale_quote.action_report_xkl_sale_quote'
        ).report_action(self)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    xkl_sub_items = fields.Text(
        string='Included Components',
        help='One component per line. Printed as bullet points under the product name in the PDF.',
    )
