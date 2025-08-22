# utils/access_control.py
from odoo import api, models
from odoo.exceptions import AccessError

class ReportAccessControl:
    """Access control utilities for reports"""
    
    @staticmethod
    def check_model_access(env, model_name, operation='read'):
        """Check if user has access to model"""
        try:
            Model = env[model_name]
            Model.check_access_rights(operation)
            return True
        except AccessError:
            return False
    
    @staticmethod
    def check_record_access(env, model_name, record_ids, operation='read'):
        """Check if user has access to specific records"""
        try:
            Model = env[model_name]
            records = Model.browse(record_ids)
            records.check_access_rights(operation)
            records.check_access_rule(operation)
            return True
        except AccessError:
            return False
    
    @staticmethod
    def filter_accessible_records(env, model_name, record_ids):
        """Filter records that user can access"""
        Model = env[model_name]
        try:
            records = Model.browse(record_ids)
            records.check_access_rule('read')
            return records.ids
        except AccessError:
            # Try individual records
            accessible_ids = []
            for record_id in record_ids:
                try:
                    record = Model.browse(record_id)
                    record.check_access_rule('read')
                    accessible_ids.append(record_id)
                except AccessError:
                    continue
            return accessible_ids