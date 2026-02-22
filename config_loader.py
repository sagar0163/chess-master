"""
Configuration Loader
===================
Load and manage game configuration
"""

import json
import os


class Config:
    """Game configuration manager"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self.get_defaults()
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_defaults(self):
        """Get default configuration"""
        return {
            "ai": {
                "enabled": True,
                "depth": 3,
                "think_time": 5
            },
            "display": {
                "show_indicators": True,
                "color": True,
                "unicode": True
            },
            "game": {
                "time_control": None,
                "save_history": True,
                "auto_save": True
            },
            "difficulty": {
                "randomness": 0.1,
                "skill_level": 10
            }
        }
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def reset(self):
        """Reset to defaults"""
        self.config = self.get_defaults()
        self.save()
