# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import api, models


class MixinPrintDocument(models.AbstractModel):
    _name = "mixin.print_document"
    _description = "Print Document Mixin"

    # Attributes related to automatically insert elemnt on form view
    _automatically_insert_print_button = False
    _print_button_xpath = "/form/header/field[@name='state']"
    _print_button_position = "before"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        if view_type == "form" and self._automatically_insert_print_button:
            doc = etree.XML(res["arch"])
            node_xpath = doc.xpath(self._print_button_xpath)
            if node_xpath:
                str_element = self.env["ir.qweb"]._render(
                    "ssi_print_mixin.button_ssi_print"
                )
                for node in node_xpath:
                    new_node = etree.fromstring(str_element)
                    if self._print_button_position == "after":
                        node.addnext(new_node)
                    elif self._print_button_position == "before":
                        node.addprevious(new_node)
                    elif self._print_button_position == "inside":
                        node.append(new_node)

            View = self.env["ir.ui.view"]

            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
            res["arch"] = new_arch
            new_fields.update(res["fields"])
            res["fields"] = new_fields
        return res
