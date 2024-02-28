{
    "name": "Sale Delivery Charges",
    "version": "16.0.1.0.4",
    "summary": "Sale Delivery Charges ",
    "version": "16.0.1.0.0",
    "depends": ['sale_management','sale',],
    "data": [
        'security/ir.model.access.csv',
        'wizard/sales_order_report_wizard.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        'report/report.xml',
        'report/sales_order_report.xml'
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
