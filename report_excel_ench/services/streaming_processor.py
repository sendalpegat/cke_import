# services/streaming_processor.py
class StreamingDataProcessor:
    """Streaming data processor for large datasets"""
    
    def __init__(self, env, chunk_size=1000):
        self.env = env
        self.chunk_size = chunk_size
    
    def process_large_dataset(self, model_name, domain, processor_func):
        """Process large dataset in chunks"""
        Model = self.env[model_name]
        
        # Get total count
        total_count = Model.search_count(domain)
        _logger.info("Processing %d records in chunks of %d", 
                    total_count, self.chunk_size)
        
        # Process in chunks
        offset = 0
        while offset < total_count:
            with MemoryManager.memory_monitor(f"chunk_{offset}"):
                # Get chunk
                chunk_records = Model.search(
                    domain, 
                    limit=self.chunk_size, 
                    offset=offset
                )
                
                # Process chunk
                yield processor_func(chunk_records)
                
                offset += self.chunk_size
                
                # Cleanup
                gc.collect()
    
    def generate_excel_streaming(self, report_config, parameters):
        """Generate Excel report using streaming approach"""
        def process_chunk(records):
            # Process records chunk
            return records.read()
        
        # Stream process data
        chunks = self.process_large_dataset(
            report_config['root_model_name'],
            report_config['domain'],
            process_chunk
        )
        
        # Yield processed chunks
        for chunk_data in chunks:
            yield chunk_data