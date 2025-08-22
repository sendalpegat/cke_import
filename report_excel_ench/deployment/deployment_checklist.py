# deployment/deployment_checklist.py
class DeploymentChecklist:
    """Deployment checklist for Report Excel module"""
    
    @staticmethod
    def run_pre_deployment_checks(env):
        """Run pre-deployment checks"""
        checks = []
        
        # Database checks
        checks.append(DeploymentChecklist._check_database_version(env))
        checks.append(DeploymentChecklist._check_dependencies(env))
        checks.append(DeploymentChecklist._check_disk_space())
        checks.append(DeploymentChecklist._check_memory_available())
        
        # Security checks
        checks.append(DeploymentChecklist._check_file_permissions())
        checks.append(DeploymentChecklist._check_temp_directory())
        
        return checks
    
    @staticmethod
    def run_post_deployment_checks(env):
        """Run post-deployment checks"""
        checks = []
        
        # Functionality checks
        checks.append(DeploymentChecklist._test_report_generation(env))
        checks.append(DeploymentChecklist._test_api_endpoints(env))
        checks.append(DeploymentChecklist._test_security_features(env))
        
        # Performance checks
        checks.append(DeploymentChecklist._test_performance(env))
        checks.append(DeploymentChecklist._test_memory_usage(env))
        
        return checks
    
    @staticmethod
    def _check_database_version(env):
        """Check database version compatibility"""
        try:
            env.cr.execute("SELECT version()")
            version = env.cr.fetchone()[0]
            
            return {
                'check': 'Database Version',
                'status': 'passed',
                'message': f'PostgreSQL version: {version}',
                'details': version
            }
        except Exception as e:
            return {
                'check': 'Database Version',
                'status': 'failed',
                'message': f'Failed to check database version: {e}',
                'details': str(e)
            }
    
    @staticmethod
    def _check_dependencies(env):
        """Check required Python dependencies"""
        required_packages = [
            'openpyxl',
            'xlsxwriter', 
            'pillow',
            'lxml'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            return {
                'check': 'Dependencies',
                'status': 'failed',
                'message': f'Missing packages: {", ".join(missing_packages)}',
                'details': missing_packages
            }
        else:
            return {
                'check': 'Dependencies',
                'status': 'passed',
                'message': 'All required packages are installed',
                'details': required_packages
            }
    
    @staticmethod
    def _check_disk_space():
        """Check available disk space"""
        import shutil
        
        try:
            total, used, free = shutil.disk_usage('/')
            free_gb = free // (1024**3)
            
            if free_gb < 5:  # Less than 5GB
                status = 'warning'
                message = f'Low disk space: {free_gb}GB available'
            elif free_gb < 1:  # Less than 1GB
                status = 'failed'
                message = f'Critical disk space: {free_gb}GB available'
            else:
                status = 'passed'
                message = f'Sufficient disk space: {free_gb}GB available'
            
            return {
                'check': 'Disk Space',
                'status': status,
                'message': message,
                'details': {'total_gb': total // (1024**3), 'free_gb': free_gb}
            }
        except Exception as e:
            return {
                'check': 'Disk Space',
                'status': 'failed',
                'message': f'Failed to check disk space: {e}',
                'details': str(e)
            }
    
    @staticmethod
    def _test_report_generation(env):
        """Test basic report generation"""
        try:
            # Create a simple test report
            test_report = env['report.excel'].create({
                'name': 'Deployment Test Report',
                'root_model_id': env.ref('base.model_res_partner').id,
                'sheet_reference': 'Sheet1'
            })
            
            # Try to generate
            result = test_report.generate_excel_report(test_report.id, {})
            
            # Clean up
            test_report.unlink()
            
            if result.get('type') == 'ir.actions.act_url':
                return {
                    'check': 'Report Generation',
                    'status': 'passed',
                    'message': 'Report generation test successful',
                    'details': result
                }
            else:
                return {
                    'check': 'Report Generation',
                    'status': 'failed',
                    'message': 'Report generation test failed',
                    'details': result
                }
                
        except Exception as e:
            return {
                'check': 'Report Generation',
                'status': 'failed',
                'message': f'Report generation test error: {e}',
                'details': str(e)
            }