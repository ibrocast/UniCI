"""
UniCI Configuration Manager
Handles non-sensitive configuration data (e.g., URLs, last-used values).
Sensitive data (API tokens) is handled by keyring in settings_tab.py.
"""
import json
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    """
    Manages loading and saving of non-sensitive JSON configuration.
    """
    def __init__(self):
        self.config_data = self.load_config()

    def load_config(self):
        """Loads config.json from disk."""
        if not os.path.exists(CONFIG_FILE):
            # Create a default config if one doesn't exist
            default_config = {
                "jenkins_url": "",
                "gitlab_url": "https://gitlab.com",
                "github_repo": ""
            }
            self.save_config(default_config)
            return default_config

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not decode {CONFIG_FILE}. Reverting to default.")
            return {} # Return empty dict to avoid crash, will be repopulated

    def save_config(self, data=None):
        """Saves the current config data to config.json."""
        if data is None:
            data = self.config_data

        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error: Could not write to {CONFIG_FILE}: {e}")

    def get_setting(self, key, default=None):
        """Gets a specific setting from the config."""
        return self.config_data.get(key, default)

    def set_setting(self, key, value):
        """Sets a specific setting and saves to disk."""
        self.config_data[key] = value
        self.save_config()