# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinMasterData(models.AbstractModel):
    _name = "mixin.master_data"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
        "mixin.print_document",
        "mixin.sequence",
    ]
    _description = "Mixin for Master Data"
    _field_name_string = "Name"
    _show_code_on_display_name = False
    _automatically_insert_print_button = True
    _print_button_xpath = "/form/header"
    _print_button_position = "inside"

    @api.model
    def _get_field_name_string(self):
        return self._field_name_string

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "code" not in default:
            default["code"] = _("%s (copy)", self.code)
        return super(MixinMasterData, self).copy(default=default)

    @api.constrains("code")
    def _check_duplicate_code(self):
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("code", "!=", "/"),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                error_message = """
                Document Type: %s
                Context: Create or update document
                Database ID: %s
                Problem: Dupilicate code
                Solution: Change code
                """ % (
                    self._description.lower(),
                    self.id,
                )
                raise UserError(error_message)

    def action_generate_code(self):
        for record in self.sudo():
            record._create_sequence()

    def action_reset_code(self):
        for record in self.sudo():
            record.write(
                {
                    "code": "/",
                }
            )

    def name_get(self):
        result = []
        for record in self:
            if self._show_code_on_display_name:
                name = "[%s] %s" % (record.code, record.name)
            else:
                name = record.name
            result.append((record.id, name))
        return result
