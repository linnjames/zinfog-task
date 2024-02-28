from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class ActionSaleReportWizard(models.TransientModel):
    _name = 'sales.order.report'

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="TO Date", required=True)



    def action_print(self):
        if self.from_date > self.to_date:
            raise UserError(_("From Date is Greater Than To Date"))

        filter_cdtn = '''WHERE so.state = 'sale' AND so.validity_date BETWEEN %s AND %s '''
        params = (self.from_date.strftime("%Y-%m-%d 00:00:00"), self.to_date.strftime("%Y-%m-%d 23:59:59"))

        cdtn = filter_cdtn
        cdtn_params = params

        query = """
            SELECT rp.id AS rp_id, rp.name AS rp_name, rp.phone AS phone,
            so.id AS si_id, so.name AS si_name,
            so.client_order_ref AS purchase_name,
            pt.name AS pt_name, pt.list_price AS pt_list_price,
            pt.standard_price AS pt_standard_price,
            sol.product_id AS product,
            uom.id AS uom_name,
            sol.product_uom_qty AS total_qty
            FROM sale_order_line sol
            LEFT JOIN sale_order so ON sol.order_id = so.id
            LEFT JOIN uom_uom uom ON sol.product_uom = uom.id
            LEFT JOIN res_partner rp ON so.partner_id = rp.id
            LEFT JOIN product_product pp ON sol.product_id = pp.id
            LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
            {}
        """.format(filter_cdtn)

        self._cr.execute(query, params)
        move_ids = self.env.cr.dictfetchall()

        if not move_ids:
            raise UserError(_("Nothing to print."))

        for move_id in move_ids:
            product_name = move_id['pt_name']
            if isinstance(product_name, dict):
                # If the product name is a dictionary, retrieve the value for the current language
                product_name = product_name.get(self.env.lang, '')
            move_id['pt_name'] = product_name.strip() if product_name else ''

        lens = []
        for i in move_ids:
            lens.append({
                'customer_id': i['rp_id'],
                'customer': i['rp_name'],
                'phone': i['phone'],
            })

        no_dup = []
        for j in lens:
            if j not in no_dup:
                no_dup.append(j)

        sort_code = sorted(no_dup, key=lambda s: s['customer'])

        data = {
            'model': self._name,
            'ids': self.ids,
            'vals': move_ids,
            'cust_code': sort_code,
            'from_date': self.from_date.strftime("%d-%m-%Y"),
            'to_date': self.to_date.strftime("%d-%m-%Y"),
            'company': self.env.company.name,
        }

        print("lllllllllllllllllll", data)
        return self.env.ref('sale_delivery_charges.report_sales_order_report_pdf').report_action(self, data=data)

