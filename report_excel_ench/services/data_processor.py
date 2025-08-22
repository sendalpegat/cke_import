class DataProcessorService:
    """Service for processing report data"""
    
    def __init__(self, env):
        self.env = env
    
    def extract_data(self, report_config, parameters):
        """
        Extract data for report generation
        
        Args:
            report_config (dict): Report configuration
            parameters (dict): Report parameters
            
        Returns:
            dict: Processed data for report
        """
        model_name = report_config.get('root_model_name')
        domain = self._build_domain(report_config, parameters)
        
        # Get records with optimized queries
        records = self._get_records_optimized(model_name, domain)
        
        # Process sections
        sections_data = self._process_sections(
            report_config.get('sections', []), 
            records, 
            parameters
        )
        
        return {
            'records': records,
            'sections': sections_data,
            'parameters': parameters
        }
    
    def _build_domain(self, config, parameters):
        """Build domain with parameters"""
        base_domain = config.get('domain', [])
        
        # Replace parameter placeholders
        processed_domain = []
        for item in base_domain:
            if isinstance(item, list) and len(item) == 3:
                field, operator, value = item
                if isinstance(value, str) and value.startswith('param('):
                    param_key = value[6:-1]  # Extract param key
                    param_value = parameters.get(param_key)
                    processed_domain.append([field, operator, param_value])
                else:
                    processed_domain.append(item)
            else:
                processed_domain.append(item)
        
        return processed_domain
    
    def _get_records_optimized(self, model_name, domain):
        """Get records with optimized queries"""
        Model = self.env[model_name]
        
        # Use read() for better performance
        records = Model.search(domain)
        
        # Batch read related fields
        if records:
            return records.read()
        
        return []
    
    def _process_sections(self, sections, records, parameters):
        """Process report sections"""
        processed_sections = {}
        
        for section in sections:
            section_data = self._process_single_section(
                section, records, parameters
            )
            processed_sections[section['id']] = section_data
        
        return processed_sections
    
    def _process_single_section(self, section, records, parameters):
        """Process single report section"""
        # Implementation for section processing
        return {
            'name': section.get('name'),
            'data': [],
            'fields': section.get('fields', [])
        }