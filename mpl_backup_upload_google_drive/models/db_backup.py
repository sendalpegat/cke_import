# -*- coding: utf-8 -*-
###############################################################################
#
#    Meghsundar Private Limited(<https://www.meghsundar.com>).
#
###############################################################################
import json
import logging
import socket

import pytz
import requests

import odoo
from odoo import models, fields, api, _
from odoo.addons.google_drive.models.google_drive import GoogleDrive

_logger = logging.getLogger(__name__)
import os
import datetime

try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib
try:
    import paramiko
except ImportError:
    raise ImportError(
        'Please install paramiko on your system. """sudo pip3 install paramiko"""')


def execute(connector, method, *args):
    res = False
    try:
        res = getattr(connector, method)(*args)
    except socket.error as error:
        _logger.critical('Error while executing the method "execute". Error: ' + str(error))
        raise error
    return res


class DbBackup(models.Model):
    _name = 'db.backup'
    _description = 'Backup configuration record'

    def get_db_list(self, host_name, port_number, context={}):
        uri = 'http://' + host_name + ':' + port_number
        conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
        db_list = execute(conn, 'list')
        return db_list

    def _get_database(self):
        dbName = self._cr.dbname
        return dbName

    host_name = fields.Char(String='host_name', default='localhost', required=True)
    port_number = fields.Char(String='port number', default=8069, required=True)
    name = fields.Char(String='Database Name', required=True, default=_get_database)
    folder = fields.Char('Backup Directory', required='True', default='backups')
    backup_type = fields.Selection([('zip', 'Zip'), ('dump', 'Dump')], 'Backup Type', required=True, default='zip')
    _get_database = fields.Boolean('Auto. Remove Backups', )

    def _check_db_exist(self):
        self.ensure_one()

        db_list = self.get_db_list(self.host_name, self.port_number)
        if self.name in db_list:
            return True
        return False

    @api.model
    def schedule_backup(self):
        conf_ids = self.search([])

        for rec in conf_ids:
            db_list = self.get_db_list(rec.host_name, rec.port_number)

            if rec.name in db_list:
                try:
                    if not os.path.isdir(rec.folder):
                        os.makedirs(rec.folder)
                except:
                    raise
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
                date_today = pytz.utc.localize(datetime.datetime.today()).astimezone(user_tz)
                bkp_file = '%s_%s.%s' % (rec.name, date_today.strftime('%Y-%m-%d_%H_%M_%S'), rec.backup_type)

                file_path = os.path.join(rec.folder, bkp_file)
                uri = 'http://' + rec.host_name + ':' + rec.port_number
                conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
                bkp = ''
                try:
                    fp = open(file_path, 'wb')
                    odoo.service.db.dump_db(rec.name, fp, rec.backup_type)
                    fp.close()
                except Exception as error:
                    _logger.debug(
                        "Couldn't backup database %s. Bad database administrator password for server running at http://%s:%s" % (
                            rec.name, rec.host_name, rec.port_number))
                    _logger.debug("Exact error from the exception: " + str(error))
                    continue

            else:
                _logger.debug("database %s doesn't exist on http://%s:%s" % (rec.name, rec.host_name, rec.port_number))

            self.google_drive_upload(rec, file_path, bkp_file)

    sql_constraints = [(_check_db_exist, _('Error ! No such database exists!'), [])]

    """For Google Drive"""

    gdrive_upload = fields.Boolean('Upload to Google Drive')
    drive_folder_id = fields.Char(string='Folder ID', )
    gdrive_email_notification_ids = fields.Many2many('res.users', string="Person to Notify")

    @api.depends('google_drive_authorization_code')
    def _compute_drive_uri(self):
        google_drive_uri = self.env['google.service']._get_google_token_uri('drive', scope=self.env[
            'google.drive.config'].get_google_scope())
        for config in self:
            config.google_drive_uri = google_drive_uri

    def set_values(self):
        params = self.env['ir.config_parameter'].sudo()
        authorization_code_before = params.get_param('google_drive_authorization_code')
        super(DbBackup, self).set_values()
        authorization_code = self.google_drive_authorization_code
        refresh_token = False
        if authorization_code and authorization_code != authorization_code_before:
            refresh_token = self.env['google.service'].generate_refresh_token('drive', authorization_code)
        params.set_param('google_drive_refresh_token', refresh_token)

    """Upload to GDrive"""

    def google_drive_upload(self, rec, file_path, bkp_file):
        g_drive = self.env['google.drive.config']
        access_token = GoogleDrive.get_access_token(g_drive)
        if rec.gdrive_upload:
            headers = {"Authorization": "Bearer %s" % (access_token)}
            para = {
                "name": "%s" % (str(bkp_file)),
                "parents": ["%s" % (str(rec.drive_folder_id))]
            }
            files = {
                'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                'file': open("%s" % (str(file_path)), "rb")
            }
            r = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers=headers,
                files=files
            )

            if r.status_code == 200:
                email_to = ""
                for record in rec.gdrive_email_notification_ids.mapped('login'):
                    email_to += record + ','
                    mail_pool = self.env['mail.mail']
                    values = {}
                    values.update({'email_from': self.env['res.users'].browse(self.env.uid).company_id.email})
                    values.update({'email_to': email_to})
                    values.update({'subject': '"Google Drive Upload Successful"'})
                    values.update({'body_html': '<h4>Backup Successfully Uploaded!</h4>'
                                                "<b>Backup File: %s</b>" % (str(bkp_file)) + \
                                                "<br>"
                                                "<a href='https://drive.google.com/drive/u/0/folders/%s'>Open</a></b>" % (
                                                    str(rec.drive_folder_id))
                                   })
                    values.update({'body': 'body'})
                    msg_id = mail_pool.create(values)
                    if msg_id:
                        mail_pool.send([msg_id])

            else:
                response = r.json()
                code = response['error']['code']
                message = response['error']['errors'][0]['message']
                reason = response['error']['errors'][0]['reason']
                email_to = ""
                for record in rec.gdrive_email_notification_ids.mapped('login'):
                    email_to += record + ','
                    mail_pool = self.env['mail.mail']
                    values = {}
                    values.update({'email_from': self.env['res.users'].browse(self.env.uid).company_id.email})
                    values.update({'email_to': email_to})
                    values.update({'subject': '"Google Drive Upload Unsuccessful"'})
                    values.update({'body_html': "<h3>Backup Upload Failed!</h3>"
                                                "<br>"
                                                "Backup" + (
                                                    str(bkp_file)) + " is not uploaded because of error code =  " + str(
                        code) + \
                                                "<br>"
                                                "Message = " + str(message) + \
                                                "<br>"
                                                "Reason =" + str(reason)
                                   })
                    values.update({'body': 'body'})
                    msg_id = mail_pool.create(values)
                    if msg_id:
                        mail_pool.send([msg_id])
