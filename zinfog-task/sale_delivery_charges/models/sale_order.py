from odoo import fields, models, api, _

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    delivery_charge = fields.Float('Delivery Charges', compute='_compute_delivery_charge', store=True)
    sum = fields.Float('Total')

    @api.depends('price_subtotal','delivery_charge','sum','price_total')
    def _compute_delivery_charge(self):
        for record in self:
            print("aaaaaa")
            record.delivery_charge = record.price_subtotal * 0.10
            record.sum = record.price_subtotal + record.delivery_charge



