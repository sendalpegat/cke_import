# utils/query_optimizer.py
from odoo import api, models

class QueryOptimizer:
    """Database query optimization utilities"""
    
    @staticmethod
    def batch_read_records(model, record_ids, fields=None, batch_size=1000):
        """Read records in batches for better performance"""
        if not record_ids:
            return []
        
        all_data = []
        for i in range(0, len(record_ids), batch_size):
            batch_ids = record_ids[i:i+batch_size]
            batch_records = model.browse(batch_ids)
            
            if fields:
                batch_data = batch_records.read(fields)
            else:
                batch_data = batch_records.read()
            
            all_data.extend(batch_data)
        
        return all_data
    
    @staticmethod
    def prefetch_related_fields(records, field_paths):
        """Prefetch related fields to avoid N+1 queries"""
        for path in field_paths:
            try:
                # Use mapped to trigger prefetching
                records.mapped(path)
            except Exception:
                # Ignore errors for invalid paths
                continue
    
    @staticmethod
    def optimize_domain(domain, model):
        """Optimize domain for better query performance"""
        if not domain:
            return domain
        
        optimized = []
        for item in domain:
            if isinstance(item, list) and len(item) == 3:
                field, operator, value = item
                
                # Optimize date comparisons
                if field.endswith('_date') or field.endswith('_datetime'):
                    if operator == '=' and isinstance(value, str):
                        # Convert date equality to range for better index usage
                        optimized.extend([
                            [field, '>=', value],
                            [field, '<', value + ' 23:59:59']
                        ])
                        if len(optimized) > 1:
                            optimized.insert(-2, '&')
                        continue
                
                optimized.append(item)
            else:
                optimized.append(item)
        
        return optimized