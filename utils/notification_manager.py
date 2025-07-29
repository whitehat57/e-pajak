from datetime import datetime, timedelta
from typing import List, Dict
from models.transaction import Transaction
from models.tax import TaxRecord
from config.settings import AppSettings

class NotificationManager:
    def __init__(self):
        self.settings = AppSettings()
    
    def get_upcoming_tax_deadlines(self, days_ahead: int = 30) -> List[Dict]:
        """Dapatkan daftar jatuh tempo pajak yang akan datang"""
        notifications = []
        reminder_days = self.settings.get('reminder_days', 7)
        
        # Hitung tanggal batas
        today = datetime.now().date()
        deadline_date = today + timedelta(days=days_ahead)
        
        # Tambahkan notifikasi untuk SPT Tahunan (31 Maret)
        current_year = today.year
        spt_deadline = datetime(current_year, 3, 31).date()
        if today <= spt_deadline <= deadline_date:
            days_until = (spt_deadline - today).days
            notifications.append({
                'type': 'SPT Tahunan',
                'description': f'SPT Tahunan {current_year-1} jatuh tempo',
                'deadline': spt_deadline.strftime('%Y-%m-%d'),
                'days_until': days_until,
                'priority': 'high' if days_until <= reminder_days else 'medium'
            })
        
        # Tambahkan notifikasi untuk PPN Bulanan (tanggal 15)
        for month in range(1, 13):
            ppn_deadline = datetime(current_year, month, 15).date()
            if today <= ppn_deadline <= deadline_date:
                days_until = (ppn_deadline - today).days
                notifications.append({
                    'type': 'PPN Bulanan',
                    'description': f'Pelaporan PPN bulan {month:02d}',
                    'deadline': ppn_deadline.strftime('%Y-%m-%d'),
                    'days_until': days_until,
                    'priority': 'high' if days_until <= reminder_days else 'medium'
                })
        
        # Tambahkan notifikasi untuk PPh 21 Bulanan (tanggal 20)
        for month in range(1, 13):
            pph21_deadline = datetime(current_year, month, 20).date()
            if today <= pph21_deadline <= deadline_date:
                days_until = (pph21_deadline - today).days
                notifications.append({
                    'type': 'PPh 21 Bulanan',
                    'description': f'Pelaporan PPh 21 bulan {month:02d}',
                    'deadline': pph21_deadline.strftime('%Y-%m-%d'),
                    'days_until': days_until,
                    'priority': 'high' if days_until <= reminder_days else 'medium'
                })
        
        # Urutkan berdasarkan tanggal jatuh tempo
        notifications.sort(key=lambda x: x['deadline'])
        return notifications
    
    def get_tax_summary_notifications(self) -> List[Dict]:
        """Dapatkan notifikasi ringkasan kewajiban pajak"""
        notifications = []
        
        # Hitung total PPh 21 yang belum dibayar
        from models.employee import Employee
        employees = Employee.get_all()
        total_pph21_withheld = 0
        
        for employee in employees:
            # Hitung PPh 21 untuk setiap pegawai (simplified)
            from services.pp21_calculator import PPh21Calculator
            calculator = PPh21Calculator(employee, 0, False)
            result = calculator.calculate_with_npwp_discount()
            total_pph21_withheld += result['final_tax']
        
        notifications.append({
            'type': 'Ringkasan Pajak',
            'description': f'Total PPh 21 terutang tahun ini: Rp {total_pph21_withheld:,.0f}',
            'priority': 'info'
        })
        
        # Hitung PPN terutang
        transactions = Transaction.get_all()
        ppn_masukan = sum(t.ppn_amount for t in transactions if t.type == "belanja")
        ppn_keluaran = sum(t.ppn_amount for t in transactions if t.type == "penjualan")
        ppn_terutang = ppn_keluaran - ppn_masukan
        
        notifications.append({
            'type': 'Ringkasan Pajak',
            'description': f'PPN terutang: Rp {ppn_terutang:,.0f}',
            'priority': 'info'
        })
        
        return notifications
    
    def get_all_notifications(self) -> List[Dict]:
        """Dapatkan semua notifikasi"""
        notifications = []
        notifications.extend(self.get_upcoming_tax_deadlines())
        notifications.extend(self.get_tax_summary_notifications())
        return notifications
    
    def format_notification_message(self, notification: Dict) -> str:
        """Format pesan notifikasi"""
        if notification['type'] == 'Ringkasan Pajak':
            return f"📊 {notification['description']}"
        else:
            priority_emoji = {
                'high': '🚨',
                'medium': '⚠️',
                'info': 'ℹ️'
            }
            emoji = priority_emoji.get(notification['priority'], '🔔')
            return f"{emoji} [{notification['type']}] {notification['description']} (jatuh tempo dalam {notification['days_until']} hari)"