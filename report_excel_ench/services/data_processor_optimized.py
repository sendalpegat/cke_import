# services/data_processor_optimized.py
class OptimizedDataProcessor(DataProcessorService):
    """Optimized data processor with caching and batching"""
    
    def __init__(self, env):
        super().__init__(env)
        self.cache = report_cache
        self.query_optimizer = QueryOptimizer()
    
    def extract_data(self, report_config, parameters):
        """Extract data with caching and optimization"""
        # Generate cache key
        cache_key = self.cache.generate_key(
            'report_data',
            report_config.get('id'),
            parameters
        )
        
        # Try to get from cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Extract data with optimizations
        data = self._extract_data_optimized(report_config, parameters)
        
        # Cache the result
        self.cache.set(cache_key, data)
        
        return data
    
    def _extract_data_optimized(self, report_config, parameters):
        """Optimized data extraction"""
        model_name = report_config.get('root_model_name')
        domain = self._build_domain(report_config, parameters)
        
        # Optimize domain
        domain = self.query_optimizer.optimize_domain(domain, model_name)
        
        # Get record IDs first (lighter query)
        Model = self.env[model_name]
        record_ids = Model.search(domain).ids
        
        # Limit records if needed
        max_records = report_config.get('max_records', 10000)
        if len(record_ids) > max_records:
            record_ids = record_ids[:max_records]
        
        # Batch read records
        fields_to_read = self._get_required_fields(report_config)
        records_data = self.query_optimizer.batch_read_records(
            Model, record_ids, fields_to_read
        )
        
        # Process sections with optimization
        sections_data = self._process_sections_optimized(
            report_config.get('sections', []),
            records_data,
            parameters
        )
        
        return {
            'records': records_data,
            'sections': sections_data,
            'parameters': parameters
        }
    
    def _get_required_fields(self, report_config):
        """Get list of fields required for the report"""
        fields = set(['id'])  # Always include ID
        
        sections = report_config.get('sections', [])
        for section in sections:
            for field_config in section.get('fields', []):
                field_selector = field_config.get('model_field_selector', '')
                if field_selector:
                    # Extract root field name
                    root_field = field_selector.split('.')[0]
                    fields.add(root_field)
        
        return list(fields)
    
    def _process_sections_optimized(self, sections, records_data, parameters):
        """Process sections with optimization"""
        processed_sections = {}
        
        # Create lookup dict for faster access
        records_lookup = {r['id']: r for r in records_data}
        
        for section in sections:
            section_data = self._process_section_optimized(
                section, records_lookup, parameters
            )
            processed_sections[section['id']] = section_data
        
        return processed_sections
    
    def _process_section_optimized(self, section, records_lookup, parameters):
        """Process single section with optimization"""
        return {
            'name': section.get('name'),
            'data': list(records_lookup.values()),
            'fields': section.get('fields', [])
        }