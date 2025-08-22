# models/report_excel_monitoring.py
from odoo import api, fields, models
from datetime import datetime, timedelta

class ReportExcelMonitoring(models.Model):
    _name = 'report.excel.monitoring'
    _description = 'Excel Report Monitoring'
    _auto = False
    
    report_id = fields.Many2one('report.excel', string='Report')
    user_id = fields.Many2one('res.users', string='User')
    generation_date = fields.Datetime(string='Generation Date')
    execution_time = fields.Float(string='Execution Time (seconds)')
    record_count = fields.Integer(string='Record Count')
    file_size = fields.Integer(string='File Size (bytes)')
    success = fields.Boolean(string='Success')
    error_message = fields.Text(string='Error Message')
    
    @api.model
    def get_report_statistics(self, days=30):
        """Get report generation statistics"""
        domain_date = datetime.now() - timedelta(days=days)
        
        self.env.cr.execute("""
            SELECT 
                r.name as report_name,
                COUNT(*) as total_generations,
                AVG(CASE WHEN m.success THEN m.execution_time END) as avg_execution_time,
                SUM(CASE WHEN m.success THEN 1 ELSE 0 END) as successful_generations,
                SUM(CASE WHEN NOT m.success THEN 1 ELSE 0 END) as failed_generations
            FROM report_excel_monitoring m
            JOIN report_excel r ON r.id = m.report_id
            WHERE m.generation_date >= %s
            GROUP BY r.id, r.name
            ORDER BY total_generations DESC
        """, (domain_date,))
        
        return self.env.cr.dictfetchall()
    
    @api.model
    def get_performance_trends(self, report_id=None, days=30):
        """Get performance trends for reports"""
        domain_date = datetime.now() - timedelta(days=days)
        
        where_clause = "WHERE m.generation_date >= %s"
        params = [domain_date]
        
        if report_id:
            where_clause += " AND m.report_id = %s"
            params.append(report_id)
        
        self.env.cr.execute(f"""
            SELECT 
                DATE(m.generation_date) as date,
                AVG(m.execution_time) as avg_execution_time,
                MAX(m.execution_time) as max_execution_time,
                COUNT(*) as total_generations,
                SUM(CASE WHEN m.success THEN 1 ELSE 0 END) as successful_generations
            FROM report_excel_monitoring m
            {where_clause}
            GROUP BY DATE(m.generation_date)
            ORDER BY date DESC
        """, params)
        
        return self.env.cr.dictfetchall()