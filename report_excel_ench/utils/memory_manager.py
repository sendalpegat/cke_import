# utils/memory_manager.py
import gc
import psutil
import os
from contextlib import contextmanager
import logging

_logger = logging.getLogger(__name__)

class MemoryManager:
    """Memory management utilities"""
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB
    
    @staticmethod
    def check_memory_limit(limit_mb=1024):
        """Check if memory usage exceeds limit"""
        current_usage = MemoryManager.get_memory_usage()
        if current_usage > limit_mb:
            gc.collect()  # Force garbage collection
            current_usage = MemoryManager.get_memory_usage()
            
            if current_usage > limit_mb:
                _logger.warning(
                    "Memory usage (%.2f MB) exceeds limit (%.2f MB)",
                    current_usage, limit_mb
                )
                return False
        return True
    
    @staticmethod
    @contextmanager
    def memory_monitor(operation_name="operation"):
        """Context manager to monitor memory usage"""
        start_memory = MemoryManager.get_memory_usage()
        _logger.info("Starting %s - Memory: %.2f MB", operation_name, start_memory)
        
        try:
            yield
        finally:
            end_memory = MemoryManager.get_memory_usage()
            memory_diff = end_memory - start_memory
            _logger.info(
                "Finished %s - Memory: %.2f MB (diff: %+.2f MB)",
                operation_name, end_memory, memory_diff
            )
            
            # Force cleanup if memory increased significantly
            if memory_diff > 100:  # 100MB threshold
                gc.collect()