# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinProductProductM2OConfigurator(models.AbstractModel):
    _name = "mixin.product_product_m2o_configurator"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "product.product Many2one Configurator Mixin"

    _product_product_m2o_configurator_insert_form_element_ok = False
    _product_product_m2o_configurator_form_xpath = False

    product_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Product Selection Method",
        required=True,
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Products",
    )
    product_domain = fields.Text(default="[]", string="Product Domain")
    product_python_code = fields.Text(
        default="result = []", string="Product Python Code"
    )

    @ssi_decorator.insert_on_form_view()
    def _product_product_m2o_configurator_insert_form_element(self, view_arch):
        # TODO
        template_xml = "ssi_product."
        template_xml += "product_product_m2o_configurator_template"
        if self._product_product_m2o_configurator_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._product_product_m2o_configurator_form_xpath,
                position="inside",
            )
        return view_arch
