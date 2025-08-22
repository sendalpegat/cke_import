# tests/test_performance.py
class TestPerformance(TransactionCase):
    """Test Performance Optimizations"""
    
    def setUp(self):
        super().setUp()
        # Create test records
        self.partners = self.env['res.partner'].create([
            {'name': f'Test Partner {i}', 'email': f'test{i}@example.com'}
            for i in range(100)
        ])
    
    def test_batch_read_performance(self):
        """Test batch read performance"""
        from ..utils.query_optimizer import QueryOptimizer
        
        import time
        start_time = time.time()
        
        # Test batch read
        data = QueryOptimizer.batch_read_records(
            self.env['res.partner'],
            self.partners.ids,
            ['name', 'email'],
            batch_size=50
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertEqual(len(data), 100)
        self.assertLess(execution_time, 5.0)  # Should complete in under 5 seconds
    
    def test_cache_functionality(self):
        """Test cache functionality"""
        from ..services.cache_service import CacheService
        
        cache = CacheService(max_size=10, ttl=60)
        
        # Test set and get
        cache.set('test_key', 'test_value')
        self.assertEqual(cache.get('test_key'), 'test_value')
        
        # Test cache miss
        self.assertIsNone(cache.get('non_existent_key'))
        
        # Test cache invalidation
        cache.invalidate()
        self.assertIsNone(cache.get('test_key'))