# services/cache_service.py
import time
import hashlib
import json
from collections import OrderedDict
from threading import Lock

class CacheService:
    """Caching service for report data"""
    
    def __init__(self, max_size=1000, ttl=3600):
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()
        self.timestamps = {}
        self.lock = Lock()
    
    def get(self, key):
        """Get item from cache"""
        with self.lock:
            if key not in self.cache:
                return None
            
            # Check if expired
            if self._is_expired(key):
                self._remove(key)
                return None
            
            # Move to end (LRU)
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
    
    def set(self, key, value):
        """Set item in cache"""
        with self.lock:
            # Remove if exists
            if key in self.cache:
                self.cache.pop(key)
            
            # Add new item
            self.cache[key] = value
            self.timestamps[key] = time.time()
            
            # Remove oldest if over limit
            while len(self.cache) > self.max_size:
                oldest_key = next(iter(self.cache))
                self._remove(oldest_key)
    
    def invalidate(self, pattern=None):
        """Invalidate cache entries"""
        with self.lock:
            if pattern is None:
                self.cache.clear()
                self.timestamps.clear()
            else:
                keys_to_remove = [
                    key for key in self.cache.keys()
                    if pattern in key
                ]
                for key in keys_to_remove:
                    self._remove(key)
    
    def _is_expired(self, key):
        """Check if cache entry is expired"""
        if key not in self.timestamps:
            return True
        return time.time() - self.timestamps[key] > self.ttl
    
    def _remove(self, key):
        """Remove entry from cache"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
    
    @staticmethod
    def generate_key(prefix, *args, **kwargs):
        """Generate cache key from arguments"""
        key_data = {
            'prefix': prefix,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()

# Global cache instance
report_cache = CacheService()