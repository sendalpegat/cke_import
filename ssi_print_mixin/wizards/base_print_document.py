# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BasePrintDocument(models.TransientModel):
    _name = "base.print_document"
    _description = "Select Report To Print"

    @api.model
    def _compute_allowed_print_action_ids(self):
        result = []
        object = self._get_object()
        obj_action_report = self.env["ir.actions.report"]
        active_model = self.env.context.get("active_model", "")
        criteria = [("model_id.model", "=", active_model)]
        report_ids = obj_action_report.search(criteria)
        if report_ids:
            for report in report_ids:
                allowed_print = self._check_allowed_print(report)
                policy = report._evaluate_print_python_code(object)
                if allowed_print and policy:
                    result.append(report.id)
        return result

    allowed_print_action_ids = fields.Many2many(
        string="Allowed Print Action",
        comodel_name="ir.actions.report",
        default=lambda self: self._compute_allowed_print_action_ids(),
        relation="rel_print_document_2_action_report",
        column1="wizard_id",
        column2="report_action_id",
    )

    report_action_id = fields.Many2one(
        string="Report Template",
        comodel_name="ir.actions.report",
    )

    def _check_allowed_print(self, object):
        result = False
        user = self.env.user
        is_superuser = self.env.is_superuser()
        if is_superuser:
            result = True
        if object.groups_id:
            user_group_ids = user.groups_id.ids
            if set(object.groups_id.ids) & set(user_group_ids):
                result = True
        else:
            result = True
        return result

    def _get_object(self):
        active_id = self.env.context.get("active_id", False)
        active_model = self.env.context.get("active_model", "")
        # TODO: Assert when invalid active_id or active_model
        object = self.env[active_model].browse([active_id])[0]
        return object

    def action_print(self):
        if self.report_action_id:
            object = self._get_object()
            report_action = self.report_action_id.report_action(object)
            report_action.update({"close_on_report_download": True})
            return report_action
        else:
            raise UserError(_("No Report Selected"))
