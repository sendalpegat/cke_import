# See LICENSE file for full copyright and licensing details.
import odoo
from odoo.http import request


class Controller(odoo.addons.bus.controllers.main.BusController):
    # override to add channels
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'popup.reminder'))
        poll = super(Controller, self)._poll(dbname, channels, last, options)
        return poll