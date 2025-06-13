{
    "name": "Purchase Advance Payment",
    "version": "14.0.3.09062025",
    "author": "Forgeflow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/purchase-workflow",
    "category": "Purchase",
    "license": "AGPL-3",
    "summary": "Allow to add advance payments on purchase orders",
    "depends": ["purchase", "cke_vendor_child"],
    "data": [
        "wizard/purchase_advance_payment_wizard_view.xml",
        "wizard/vendor_bill_advance_payment_wizard_view.xml",
        "views/account_move_tree_view.xml",
        "views/purchase_view.xml",
        "views/account_move_commercial_invoice_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
