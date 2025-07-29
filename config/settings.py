import json
import os
from datetime import datetime
from typing import Dict, Any

class AppSettings:
    def __init__(self):
        self.settings_file = "config/app_settings.json"
        self.default_settings = {
            "company_name": "Perusahaan Saya",
            "company_npwp": "",
            "company_address": "",
            "default_currency": "IDR",
            "ppn_rate": 0.11,
            "corporate_tax_rate": 0.25,
            "reminder_days": 7,
            "auto_backup": True,
            "backup_frequency": "weekly",
            "theme": "default",
            "language": "id",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Muat pengaturan dari file, jika tidak ada buat dengan default"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Pastikan semua key default ada
                    for key, value in self.default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.default_settings.copy()
        else:
            # Buat direktori config jika belum ada
            config_dir = os.path.dirname(self.settings_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            self.save_settings(self.default_settings)
            return self.default_settings.copy()
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Simpan pengaturan ke file"""
        try:
            settings['updated_at'] = datetime.now().isoformat()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Dapatkan nilai pengaturan"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set nilai pengaturan"""
        self.settings[key] = value
        return self.save_settings(self.settings)
    
    def get_all(self) -> Dict[str, Any]:
        """Dapatkan semua pengaturan"""
        return self.settings.copy()
    
    def reset_to_default(self) -> bool:
        """Reset pengaturan ke default"""
        self.settings = self.default_settings.copy()
        return self.save_settings(self.settings)
    
    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        """Update beberapa pengaturan sekaligus"""
        self.settings.update(new_settings)
        return self.save_settings(self.settings)