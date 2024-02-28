from odoo import fields, models, api, _

class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    invoice_delivery_charge = fields.Float('Delivery Charges', compute='_compute_invoice_delivery_charge', store=True)
    total = fields.Float('Total')

    @api.depends('price_subtotal','invoice_delivery_charge')
    def _compute_invoice_delivery_charge(self):
        for record in self:
            print("aaaaaa")
            record.invoice_delivery_charge = record.price_subtotal * 0.10
            record.total = record.price_subtotal + record.invoice_delivery_charge


