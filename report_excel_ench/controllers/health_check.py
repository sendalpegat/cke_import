# deployment/health_check.py
class HealthCheckEndpoint:
    """Health check endpoint for monitoring"""
    
    @http.route('/health/excel-reports', type='json', auth='none', csrf=False)
    def health_check(self):
        """Health check endpoint"""
        try:
            # Basic functionality check
            env = request.env(su=True)
            
            checks = {
                'database': self._check_database_connection(env),
                'cache': self._check_cache_service(),
                'temp_directory': self._check_temp_directory(),
                'memory': self._check_memory_usage(),
            }
            
            # Overall status
            all_passed = all(check['status'] == 'passed' for check in checks.values())
            overall_status = 'healthy' if all_passed else 'unhealthy'
            
            return {
                'status': overall_status,
                'timestamp': datetime.now().isoformat(),
                'checks': checks,
                'version': '1.4.0'
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'version': '1.4.0'
            }
    
    def _check_database_connection(self, env):
        """Check database connection"""
        try:
            env.cr.execute("SELECT 1")
            return {'status': 'passed', 'message': 'Database connection OK'}
        except Exception as e:
            return {'status': 'failed', 'message': f'Database error: {e}'}
    
    def _check_cache_service(self):
        """Check cache service"""
        try:
            from ..services.cache_service import report_cache
            test_key = 'health_check_test'
            report_cache.set(test_key, 'test_value')
            value = report_cache.get(test_key)
            
            if value == 'test_value':
                return {'status': 'passed', 'message': 'Cache service OK'}
            else:
                return {'status': 'failed', 'message': 'Cache service not working'}
        except Exception as e:
            return {'status': 'failed', 'message': f'Cache error: {e}'}
    
    def _check_temp_directory(self):
        """Check temp directory access"""
        try:
            import tempfile
            import os
            
            temp_dir = tempfile.gettempdir()
            test_file = os.path.join(temp_dir, 'health_check_test.txt')
            
            # Write test
            with open(test_file, 'w') as f:
                f.write('test')
            
            # Read test
            with open(test_file, 'r') as f:
                content = f.read()
            
            # Clean up
            os.remove(test_file)
            
            if content == 'test':
                return {'status': 'passed', 'message': 'Temp directory OK'}
            else:
                return {'status': 'failed', 'message': 'Temp directory read/write failed'}
                
        except Exception as e:
            return {'status': 'failed', 'message': f'Temp directory error: {e}'}
    
    def _check_memory_usage(self):
        """Check memory usage"""
        try:
            from ..utils.memory_manager import MemoryManager
            memory_mb = MemoryManager.get_memory_usage()
            
            if memory_mb > 2048:  # 2GB threshold
                return {'status': 'warning', 'message': f'High memory usage: {memory_mb:.2f}MB'}
            else:
                return {'status': 'passed', 'message': f'Memory usage OK: {memory_mb:.2f}MB'}
                
        except Exception as e:
            return {'status': 'failed', 'message': f'Memory check error: {e}'}