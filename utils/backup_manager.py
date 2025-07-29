import sqlite3
import shutil
import os
from datetime import datetime
from typing import List, Dict
from config.settings import AppSettings

class BackupManager:
    def __init__(self, db_path: str = "tax_manager.db"):
        self.db_path = db_path
        self.backup_dir = "backups"
        self.settings = AppSettings()
        
        # Buat direktori backup jika belum ada
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, backup_name: str = None) -> str:
        """Buat backup database"""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.db"
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copy2(self.db_path, backup_path)
            return backup_path
        except Exception as e:
            raise Exception(f"Gagal membuat backup: {e}")
    
    def restore_backup(self, backup_filename: str) -> bool:
        """Restore database dari backup"""
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            raise Exception("File backup tidak ditemukan")
        
        try:
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            raise Exception(f"Gagal restore backup: {e}")
    
    def list_backups(self) -> List[Dict]:
        """Dapatkan daftar backup yang tersedia"""
        backups = []
        
        if os.path.exists(self.backup_dir):
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.db'):
                    file_path = os.path.join(self.backup_dir, filename)
                    file_stat = os.stat(file_path)
                    backups.append({
                        'filename': filename,
                        'filepath': file_path,
                        'size': file_stat.st_size,
                        'modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        # Urutkan berdasarkan tanggal modifikasi (terbaru dulu)
        backups.sort(key=lambda x: x['modified'], reverse=True)
        return backups
    
    def delete_backup(self, filename: str) -> bool:
        """Hapus file backup"""
        file_path = os.path.join(self.backup_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def auto_backup(self) -> str:
        """Buat backup otomatis berdasarkan pengaturan"""
        if not self.settings.get('auto_backup', True):
            return None
        
        # Buat backup dengan nama berdasarkan frekuensi
        frequency = self.settings.get('backup_frequency', 'weekly')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"auto_{frequency}_{timestamp}.db"
        
        return self.create_backup(backup_name)