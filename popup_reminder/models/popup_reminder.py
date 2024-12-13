# See LICENSE file for full copyright and licensing details.

import datetime
import time
import odoo
from odoo.osv import expression
from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.http import request
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.safe_eval import safe_eval, time
from odoo.tools import ustr
from psycopg2 import sql

skip_models_list = ['ir.property', 'ir.model.data', 'ir.module.module']

create_original = models.BaseModel.create
 
@api.model
@api.returns('self', lambda value: value.id)
def create(self, vals):
    record_id = create_original(self, vals)
    is_installed = self.env['ir.module.module'].sudo().search_count(
        [('name', '=', 'popup_reminder'), ('state', '=', 'installed')])
    if is_installed and self._name != 'bus.bus':
        popup_obj = self.env['popup.reminder']
        model_ids = popup_obj.sudo().search_count(
            [('model_id', '=', self._name)])
        if model_ids or self._name == "popup.reminder":
            count = popup_obj.set_notification(count=True)
            self.env['bus.bus'].sudo().sendmany(
                [[(self._cr.dbname, 'popup.reminder'), count]])
    return record_id
 
 
models.BaseModel.create = create
 
write_original = models.BaseModel.write

def write(self, vals):
    result = write_original(self, vals)
    context = dict(self._context)
    if context is None:
        context = {}
    if context.get('_force_unlink', False) or self._name in skip_models_list:
        return result
    is_installed = self.env['ir.module.module'].sudo().search_count(
        [('name', '=', 'popup_reminder'), ('state', '=', 'installed')])
    if is_installed:
        for rec in self:
            popup_obj = self.env['popup.reminder']
            model_ids = popup_obj.sudo().search_count(
                [('model_id', '=', self._name)])
            if model_ids or self._name == "popup.reminder":
                count = popup_obj.set_notification(count=True)
                self.env['bus.bus'].sudo().sendmany(
                    [[(self._cr.dbname, 'popup.reminder'), count]])
    return result
 
models.BaseModel.write = write

class PopupReminder(models.Model):
    _name = 'popup.reminder'
    _description = "Popup Reminder"

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', size=128)
    model_id = fields.Many2one('ir.model', 'Model', ondelete='cascade')
    field_id = fields.Many2one(
        'ir.model.fields',
        'Fields',
    )
    group_ids = fields.Many2many(
        'res.groups',
        'popup_res_groups',
        'group_id',
        'popup_field_id',
        'Groups')
    popup_field_ids = fields.One2many('field.sequence.list', 'popup_id',
                                      string="Display Fields")
    search_option = fields.Selection([('all', 'All'),
                                      ('days', 'Days'), ('today', 'Today'),
                                      ('current_month', 'Current Month'),
                                      ('next_month', 'Next Month'),
                                      ('as_date', 'As Date')],
                                     'Search Option',
                                     help="To use the functionality of As Date \
                                     the field needs to be in the database !")
    duration_in_days = fields.Integer('Days')
    from_today = fields.Boolean('From Today')
    user_domain = fields.Text('User Domain')

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code(
            'reminder_code')
        return super(PopupReminder, self).create(vals)
    
    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.field_id = False
        self.popup_field_ids = [(5, [])]

    def get_domain(self, tday_date, cur_month_first_date,
                   cur_month_last_date,
                   next_month_first_date, next_month_last_date, today_date):
        model_domain = []
        field_name = self.field_id.name
        model_domain.append((field_name, '!=', None))
        if self.search_option == 'current_month':
            if self.field_id.ttype in ['datetime']:
                try:
                    cur_month_last_date = datetime.datetime.strptime(
                        str(cur_month_last_date),
                        DEFAULT_SERVER_DATETIME_FORMAT
                    ).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                except:
                    cur_month_last_date = datetime.datetime.strptime(
                        str(cur_month_last_date), '%Y-%m-%d'
                    ).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                try:
                    cur_month_first_date = datetime.datetime.strptime(
                        str(cur_month_first_date), '%Y-%m-%d %H:%M:%S'
                    ).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                except:
                    cur_month_first_date = datetime.datetime.strptime(
                        str(cur_month_first_date), '%Y-%m-%d'
                    ).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            if self.from_today:
                model_domain.append((field_name,
                                     '>=', today_date))
                model_domain.append((field_name,
                                     '<=', cur_month_last_date))
            else:
                model_domain.append((field_name,
                                     '>=', cur_month_first_date))
                model_domain.append((field_name,
                                     '<=', cur_month_last_date))

        if self.search_option == 'next_month':
            if self.field_id.ttype in ['datetime']:
                next_month_first_date = next_month_first_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT)
                next_month_last_date = next_month_last_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT)
            model_domain.append((field_name, '>=', next_month_first_date))
            model_domain.append((field_name, '<=', next_month_last_date))

        if self.search_option == 'days':
            next_date = False
            if self.duration_in_days > 0:
                if self.field_id.ttype in ['datetime']:
                    next_date = datetime.date.today() + \
                        datetime.timedelta(days=self.duration_in_days)
                    next_date = next_date.strftime('%Y-%m-%d 23:59:59')
                if not next_date:
                    next_date = datetime.date.today() + \
                        datetime.timedelta(days=self.duration_in_days)
                    next_date = next_date.strftime('%Y-%m-%d 23:59:59')
                if self.from_today:
                    model_domain.append((field_name, '>=', today_date))
                else:
                    tday_date = tday_date.strftime('%Y-%m-%d 23:59:59')
                    model_domain.append((field_name, '>', tday_date))
                model_domain.append((field_name, '<=', next_date))
            else:
                if self.field_id.ttype in ['datetime']:
                    next_date = datetime.date.today() + \
                        datetime.timedelta(days=self.duration_in_days)
                    next_date = next_date.strftime(
                        DEFAULT_SERVER_DATETIME_FORMAT)
                if not next_date:
                    next_date = datetime.date.today() + \
                        datetime.timedelta(days=self.duration_in_days)
                    next_date = next_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                if self.from_today:
                    tday_date = tday_date.strftime('%Y-%m-%d 23:59:59')
                    model_domain.append((field_name, '<=', tday_date))
                else:
                    model_domain.append((field_name, '<', today_date))
                model_domain.append((field_name, '>=', next_date))
        if self.search_option == 'today':
            lastHourDateTime = tday_date + relativedelta(hours=23,
                                                         minute=59, second=59)
            lastHourDateTime = lastHourDateTime.strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
            model_domain.append((field_name, '>=', today_date))
            model_domain.append((field_name, '<=', lastHourDateTime))

        user_domain_val = []
        eval_context = self._eval_context()
        if self.user_domain:
            try:
                user_domain_val = expression.normalize_domain(
                    safe_eval(self.user_domain, eval_context))
            except Exception as e:
                raise UserError(_('This domain is syntactically not correct: %s') % e)
        model_domain.extend(user_domain_val)
        return model_domain

    @api.model
    def _eval_context(self):
        """Returns a dictionary to use as evaluation context for
           popup reminder domains."""
        return {'user': request.env.user, 'time': time}

    @api.model
    def get_total_data(self):
        tot_count = 0
        result = {'tot_count': 0, 'model_dict': {}}
        public_user = request.env.user.has_group('base.group_public')
        if not public_user:
            model_dict = {}
            tday_date = datetime.date.today()
            cur_month_first_date = tday_date + relativedelta(day=1)
            cur_month_last_date = tday_date + relativedelta(
                day=1, months=+1, days=-1)
            next_month_first_date = tday_date + relativedelta(day=1, months=+1)
            next_month_last_date = tday_date + relativedelta(
                day=1, months=+2, days=-1)
            today_date = tday_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            for data in self.search([]):
                visible = False
                if data.group_ids.mapped('users').filtered(lambda x: x.id == self.env.user.id):
                    visible = True
                if visible:
                    model_obj = self.env[data.model_id.model]
                    domain = data.get_domain(tday_date, cur_month_first_date,
                                             cur_month_last_date,
                                             next_month_first_date,
                                             next_month_last_date, today_date)
                    if data.search_option == 'as_date':
                        if data.duration_in_days:
                            tday_date = tday_date + \
                                datetime.timedelta(days=data.duration_in_days)
                        model_str= self.env[data.model_id.model].browse()._table
                        field_name = data.field_id.name
                        day = tday_date.day
                        month = tday_date.month
                        query_stmt = sql.SQL('''SELECT count(id) FROM {table_name} WHERE EXTRACT(month FROM
                        {column_name} ) = {month} AND EXTRACT(day FROM {column_name}) = {day}''').format(
                        table_name = sql.Identifier(model_str),
                        column_name = sql.Identifier(field_name),
                        month = sql.Literal(month),
                        day = sql.Literal(day))
                        self._cr.execute(query_stmt)
                        
                        count = self._cr.fetchone()
                        if count:
                            count = count[0]
                    else:
                        try:
                            count = model_obj.search_count(domain)
                        except Exception as e:
                            raise UserError(_('Domain is not set correctly: %s') % e)
                    model_dict.update({str(data.name): count})
                    tot_count += count and int(count) or 0
            result.update({'tot_count': tot_count, 'model_dict': model_dict})
        return result

    @api.model
    def get_record_header(self):
        reminder_ids = self.search([], order='sequence')
        res = []
        res_model = []
        res_data = {}
        for data in reminder_ids:
            field_list = []
            visible = False
            if data.group_ids.mapped('users').filtered(lambda x: x.id == self.env.user.id):
                visible = True
            if visible:
                res_model.append((str(data.name), data.model_id.model))
                for display_data in data.popup_field_ids:
                    sortable = 'true'
                    if display_data.ir_field_id.ttype in ['one2many',
                                                          'many2many',
                                                          'binary', 'html',
                                                          'text']:
                        sortable = 'false'
                    field_list.append((str(display_data.ir_field_id.name),
                                       ustr(display_data.ir_field_id.field_description),
                                       sortable, display_data.ir_field_id.ttype,
                                       ))
                res.append((str(data.name), field_list))
                res_data.update({'data_rec_id': data.id})
        res_data.update({'header_data': res, 'model_data': res_model})
        return res_data

    @api.model
    def set_notification(self, offset=0, limit=100, count=False,
                         order='sequence', selected_model=False):
        if count:
            return self.get_total_data().get('tot_count')
        res = []
        cr = self.env.args
        tday_date = datetime.date.today()
        cur_month_first_date = tday_date + relativedelta(day=1)
        cur_month_last_date = tday_date + relativedelta(
            day=1, months=+1, days=-1)
        next_month_first_date = tday_date + relativedelta(day=1, months=+1)
        next_month_last_date = tday_date + relativedelta(
            day=1, months=+2, days=-1)
        today_date = tday_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        
        #backend date/datetime display format
        lang = self.env['res.lang'].sudo().search(
            [('code', '=', request.env.context.get('lang'))])
        d_format = DEFAULT_SERVER_DATE_FORMAT
        dt_format = DEFAULT_SERVER_DATETIME_FORMAT
        if lang:
            d_format = lang.date_format
            dt_format = lang.date_format + " " +lang.time_format
        
        if not selected_model:
            reminder_ids = self.sudo().search([])
        else:
            reminder_ids = self.search([
                ('model_id.model', '=', selected_model)], order='sequence')
        for data in reminder_ids:
            data_ids = []

            if selected_model:
                model_obj = self.env[selected_model]
                model_str= self.env[selected_model].browse()._table
            else:
                model_obj = self.env[data.model_id.model]
                model_str= self.env[data.model_id.model].browse()._table
            user_count = 0
            if data.group_ids:
                for groups in data.group_ids:
                    for user in groups.users:
                        if self.env.user.id == user.id:
                            user_count = user_count + 1
            if user_count >= 1:
                if data.search_option == 'as_date':
                    if data.duration_in_days:
                        tday_date = tday_date + \
                            datetime.timedelta(days=data.duration_in_days)
                    field_name = data.field_id.name
                    day = tday_date.day
                    month = tday_date.month
                    order_column = field_name
                    order_type = "asc"
                    if order:
                        splits = order.split()
                        order_column = splits[0]
                        order_type = "desc" if len(splits)>1 and splits[1].lower() == "desc" else "asc"

                    query_stmt = sql.SQL("SELECT * FROM {table_name} WHERE EXTRACT(month FROM {column_name} ) \
                    = {month} AND EXTRACT(day FROM {column_name}) = {day} ORDER BY {order_column} {order_type}").format(
                        table_name = sql.Identifier(model_str),
                        column_name = sql.Identifier(field_name),
                        month = sql.Literal(month),
                        day = sql.Literal(day),
                        order_column = sql.Identifier(order_column),
                        order_type = sql.SQL(order_type))

                    self._cr.execute(query_stmt)
                    data_ids_as_date = [audit_data[0] for audit_data in
                                        self._cr.fetchall()]
                    data_ids = model_obj.browse(data_ids_as_date)
                else:
                    domain = data.get_domain(tday_date, cur_month_first_date,
                                             cur_month_last_date,
                                             next_month_first_date,
                                             next_month_last_date, today_date)
                    try:
                        data_ids = model_obj.search(domain,
                                                    limit=limit,
                                                    offset=offset,
                                                    order=order)
                    except Exception as e:
                            raise UserError(_('Domain is not set correctly: %s') % e)
                read_data = []
                field_res = {}
                for display_data in data.popup_field_ids:
                    read_data.append(str(display_data.ir_field_id.name))
                    field_res.update(
                        {str(display_data.ir_field_id.name): ustr(
                            display_data.ir_field_id.field_description)})
                model_data = []
                for data_id in data_ids:
                    model_data_element = data_id.read(read_data)
                    for key, value in model_data_element[0].items():
                        if isinstance(value, (tuple)) and len(value) == 2:
                            model_data_element[0][key] = value[1]
                        if isinstance(value, (datetime.date)):
                            model_data_element[0][key] = value.strftime(d_format)
                        if isinstance(value, (datetime.datetime)):
                            timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
                            self_tz = self.with_context(tz=timezone)
                            new_dt = fields.Datetime.context_timestamp(self_tz, fields.Datetime.from_string(value))
                            model_data_element[0][key] = new_dt.strftime(dt_format)
                    model_data.extend(model_data_element)
                res.append((str(data.name), model_data))
        return res

    @api.model
    def get_list(self, offset, order, selected_model):
        public_user = request.env.user.has_group('base.group_public')
        vals ={"record_header": [], "reminder_list": [], "model_data": []}
        if not public_user:
            rec_header = self.get_record_header()
            vals = {
                "record_header":
                    rec_header and rec_header.get('header_data') or [],
                "reminder_list":
                    self.set_notification(count=False, offset=offset, order=order,
                                          selected_model=selected_model),
                "model_data":
                    rec_header and rec_header.get('model_data') or [],
            }
        return vals


class FieldList(models.Model):
    _name = 'field.sequence.list'
    _description = "Fields"
    _order = 'sequence'
    _rec_name = 'sequence'

    sequence = fields.Integer(default=10)
    ir_field_id = fields.Many2one('ir.model.fields', string='Field name')
    popup_id = fields.Many2one('popup.reminder', required=1, ondelete='cascade')
