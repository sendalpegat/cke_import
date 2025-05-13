# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    print_python_code = fields.Text(
        string="Condition",
        help="The result of executing the expresion must be " "a boolean.",
        default="""# Available locals:\n#  - document: current record\nresult = True""",
    )

    def _get_print_localdict(self, document):
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    def _evaluate_print_python_code(self, document):
        self.ensure_one()
        result = ""
        localdict = self._get_print_localdict(document)
        try:
            safe_eval(self.print_python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except:  # noqa: E722
            result = False
        return result
