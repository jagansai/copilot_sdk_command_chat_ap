'''
The aim of this module is to provide functionality for loading from the properties file under config directory
'''

import configparser
import os
class PropertyLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.load_properties()

    def load_properties(self):
        """Load properties from the specified file."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Properties file not found: {self.file_path}")
        _ = self.config.read(self.file_path, encoding='utf-8')

    def get_property(self, section: str, key: str) -> str:
        """Get a property value by section and key."""
        try:
            return self.config[section][key]
        except KeyError as e:
            raise KeyError(f"Property '{key}' not found in section '{section}': {e}")
        
