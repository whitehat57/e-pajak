from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, FloatPrompt, IntPrompt
from rich import print as rprint
import os
from config.settings import AppSettings
from utils.backup_manager import BackupManager
from utils.notification_manager import NotificationManager

console = Console()

class SettingsMenu:
    def __init__(self):
        self.settings = AppSettings()
        self.backup_manager = BackupManager()
        self.notification_manager = NotificationManager()
    
    def show_settings_menu(self):
        while True:
            console.clear()
            console.print("[bold gray]⚙️  PENGATURAN APLIKASI[/bold gray]")
            console.print("=" * 50)
            
            menu_options = [
                "[1] 🏢 Profil Perusahaan",
                "[2] 💰 Pengaturan Pajak",
                "[3] 🔔 Pengaturan Notifikasi",
                "[4] 💾 Backup & Restore",
                "[5] 📋 Lihat Notifikasi",
                "[6] 📊 Ringkasan Sistem",
                "[7] ⚡ Reset ke Default",
                "[0] 🔙 Kembali ke Menu Utama"
            ]
            
            for option in menu_options:
                console.print(option)
            
            console.print("=" * 50)
            choice = Prompt.ask("[bold]Pilih menu[/bold]", choices=["0","1","2","3","4","5","6","7"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.company_profile_settings()
            elif choice == "2":
                self.tax_settings()
            elif choice == "3":
                self.notification_settings()
            elif choice == "4":
                self.backup_restore_menu()
            elif choice == "5":
                self.show_notifications()
            elif choice == "6":
                self.system_summary()
            elif choice == "7":
                self.reset_settings()
    
    def company_profile_settings(self):
        console.clear()
        console.print("[bold blue]🏢 PROFIL PERUSAHAAN[/bold blue]")
        console.print("=" * 50)
        
        # Tampilkan profil saat ini
        console.print("[bold]Profil Saat Ini:[/bold]")
        console.print(f"Nama Perusahaan : {self.settings.get('company_name')}")
        console.print(f"NPWP            : {self.settings.get('company_npwp') or '-'}")
        console.print(f"Alamat          : {self.settings.get('company_address') or '-'}")
        console.print(f"Mata Uang       : {self.settings.get('default_currency')}")
        
        console.print("\n" + "-" * 30)
        
        try:
            # Input data baru
            company_name = Prompt.ask("Nama Perusahaan", default=self.settings.get('company_name'))
            company_npwp = Prompt.ask("NPWP Perusahaan", default=self.settings.get('company_npwp') or "")
            company_address = Prompt.ask("Alamat Perusahaan", default=self.settings.get('company_address') or "")
            currency = Prompt.ask("Mata Uang Default", choices=["IDR", "USD", "EUR"], default=self.settings.get('default_currency'))
            
            # Simpan pengaturan
            new_settings = {
                'company_name': company_name,
                'company_npwp': company_npwp if company_npwp else "",
                'company_address': company_address if company_address else "",
                'default_currency': currency
            }
            
            if self.settings.update_settings(new_settings):
                console.print("[bold green]✅ Profil perusahaan berhasil diperbarui![/bold green]")
            else:
                console.print("[bold red]❌ Gagal memperbarui profil![/bold red]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def tax_settings(self):
        console.clear()
        console.print("[bold yellow]💰 PENGATURAN PAJAK[/bold yellow]")
        console.print("=" * 50)
        
        # Tampilkan pengaturan saat ini
        console.print("[bold]Pengaturan Pajak Saat Ini:[/bold]")
        console.print(f"Tarif PPN       : {self.settings.get('ppn_rate')*100:.1f}%")
        console.print(f"Tarif Pajak Badan: {self.settings.get('corporate_tax_rate')*100:.1f}%")
        
        console.print("\n" + "-" * 30)
        
        try:
            # Input data baru
            ppn_rate = FloatPrompt.ask("Tarif PPN (%)", default=self.settings.get('ppn_rate')*100)
            corporate_tax_rate = FloatPrompt.ask("Tarif Pajak Badan (%)", default=self.settings.get('corporate_tax_rate')*100)
            
            # Validasi input
            if not (0 <= ppn_rate <= 100):
                console.print("[bold red]❌ Tarif PPN harus antara 0-100%[/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            if not (0 <= corporate_tax_rate <= 100):
                console.print("[bold red]❌ Tarif Pajak Badan harus antara 0-100%[/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Simpan pengaturan
            new_settings = {
                'ppn_rate': ppn_rate / 100,
                'corporate_tax_rate': corporate_tax_rate / 100
            }
            
            if self.settings.update_settings(new_settings):
                console.print("[bold green]✅ Pengaturan pajak berhasil diperbarui![/bold green]")
            else:
                console.print("[bold red]❌ Gagal memperbarui pengaturan![/bold red]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def notification_settings(self):
        console.clear()
        console.print("[bold orange]🔔 PENGATURAN NOTIFIKASI[/bold orange]")
        console.print("=" * 50)
        
        # Tampilkan pengaturan saat ini
        console.print("[bold]Pengaturan Notifikasi Saat Ini:[/bold]")
        console.print(f"Hari Pengingat   : {self.settings.get('reminder_days')} hari sebelum jatuh tempo")
        console.print(f"Auto Backup      : {'Aktif' if self.settings.get('auto_backup') else 'Nonaktif'}")
        console.print(f"Frekuensi Backup : {self.settings.get('backup_frequency')}")
        
        console.print("\n" + "-" * 30)
        
        try:
            # Input data baru
            reminder_days = IntPrompt.ask("Hari Pengingat", default=self.settings.get('reminder_days'))
            auto_backup = Confirm.ask("Aktifkan Auto Backup?", default=self.settings.get('auto_backup'))
            
            if auto_backup:
                backup_frequency = Prompt.ask("Frekuensi Backup", choices=["daily", "weekly", "monthly"], default=self.settings.get('backup_frequency'))
            else:
                backup_frequency = self.settings.get('backup_frequency')
            
            # Simpan pengaturan
            new_settings = {
                'reminder_days': reminder_days,
                'auto_backup': auto_backup,
                'backup_frequency': backup_frequency
            }
            
            if self.settings.update_settings(new_settings):
                console.print("[bold green]✅ Pengaturan notifikasi berhasil diperbarui![/bold green]")
            else:
                console.print("[bold red]❌ Gagal memperbarui pengaturan![/bold red]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def backup_restore_menu(self):
        while True:
            console.clear()
            console.print("[bold purple]💾 BACKUP & RESTORE[/bold purple]")
            console.print("=" * 50)
            
            menu_options = [
                "[1] 📤 Buat Backup Manual",
                "[2] 📥 Restore dari Backup",
                "[3] 📋 Lihat Riwayat Backup",
                "[4] 🗑️  Hapus Backup",
                "[0] 🔙 Kembali"
            ]
            
            for option in menu_options:
                console.print(option)
            
            console.print("=" * 50)
            choice = Prompt.ask("[bold]Pilih menu[/bold]", choices=["0","1","2","3","4"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.create_manual_backup()
            elif choice == "2":
                self.restore_from_backup()
            elif choice == "3":
                self.show_backup_history()
            elif choice == "4":
                self.delete_backup()
    
    def create_manual_backup(self):
        console.clear()
        console.print("[bold green]📤 BUAT BACKUP MANUAL[/bold green]")
        console.print("=" * 50)
        
        try:
            backup_name = Prompt.ask("Nama backup (opsional)", default="")
            if not backup_name:
                backup_name = None
            
            backup_path = self.backup_manager.create_backup(backup_name)
            console.print(f"[bold green]✅ Backup berhasil dibuat![/bold green]")
            console.print(f"   Lokasi: {backup_path}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def restore_from_backup(self):
        console.clear()
        console.print("[bold red]📥 RESTORE DARI BACKUP[/bold red]")
        console.print("=" * 50)
        
        try:
            # Tampilkan daftar backup
            backups = self.backup_manager.list_backups()
            
            if not backups:
                console.print("[yellow]⚠️  Belum ada file backup[/yellow]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Tampilkan daftar backup
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("No", style="dim", width=4)
            table.add_column("Nama File", width=30)
            table.add_column("Tanggal", width=20)
            table.add_column("Ukuran", justify="right")
            
            for i, backup in enumerate(backups[:10], 1):  # Tampilkan maksimal 10 backup terbaru
                # Format ukuran file
                size = backup['size']
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                
                table.add_row(
                    str(i),
                    backup['filename'],
                    backup['modified'],
                    size_str
                )
            
            console.print(table)
            
            # Pilih backup
            backup_index = IntPrompt.ask("\nPilih nomor backup", choices=[str(i) for i in range(1, len(backups[:10])+1)])
            selected_backup = backups[backup_index - 1]
            
            # Konfirmasi restore
            console.print(f"\n[bold yellow]⚠️  PERINGATAN: Restore akan mengganti data saat ini![/bold yellow]")
            console.print(f"File backup: {selected_backup['filename']}")
            confirm = Confirm.ask("Lanjutkan restore?")
            
            if confirm:
                if self.backup_manager.restore_backup(selected_backup['filename']):
                    console.print("[bold green]✅ Restore berhasil![/bold green]")
                    console.print("[bold red]⚠️  Aplikasi perlu direstart untuk melihat perubahan[/bold red]")
                else:
                    console.print("[bold red]❌ Gagal melakukan restore![/bold red]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_backup_history(self):
        console.clear()
        console.print("[bold cyan]📋 RIWAYAT BACKUP[/bold cyan]")
        console.print("=" * 80)
        
        try:
            backups = self.backup_manager.list_backups()
            
            if not backups:
                console.print("[yellow]⚠️  Belum ada file backup[/yellow]")
                input("\nTekan Enter untuk kembali...")
                return
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("No", style="dim", width=4)
            table.add_column("Nama File", width=30)
            table.add_column("Tanggal", width=20)
            table.add_column("Ukuran", justify="right")
            
            for i, backup in enumerate(backups, 1):
                # Format ukuran file
                size = backup['size']
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                
                table.add_row(
                    str(i),
                    backup['filename'],
                    backup['modified'],
                    size_str
                )
            
            console.print(table)
            console.print(f"\n[bold]Total backup: {len(backups)}[/bold]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def delete_backup(self):
        console.clear()
        console.print("[bold red]🗑️  HAPUS BACKUP[/bold red]")
        console.print("=" * 50)
        
        try:
            backups = self.backup_manager.list_backups()
            
            if not backups:
                console.print("[yellow]⚠️  Belum ada file backup[/yellow]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Tampilkan daftar backup
            self.show_backup_history()
            
            # Pilih backup untuk dihapus
            backup_index = IntPrompt.ask("\nPilih nomor backup yang akan dihapus", 
                                       choices=[str(i) for i in range(1, len(backups)+1)])
            selected_backup = backups[backup_index - 1]
            
            # Konfirmasi hapus
            confirm = Confirm.ask(f"Yakin ingin menghapus '{selected_backup['filename']}'?")
            if confirm:
                if self.backup_manager.delete_backup(selected_backup['filename']):
                    console.print("[bold green]✅ Backup berhasil dihapus![/bold green]")
                else:
                    console.print("[bold red]❌ Gagal menghapus backup![/bold red]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_notifications(self):
        console.clear()
        console.print("[bold orange]🔔 NOTIFIKASI SISTEM[/bold orange]")
        console.print("=" * 80)
        
        try:
            notifications = self.notification_manager.get_all_notifications()
            
            if not notifications:
                console.print("[yellow]ℹ️  Tidak ada notifikasi[/yellow]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Kelompokkan berdasarkan prioritas
            high_priority = [n for n in notifications if n.get('priority') == 'high']
            medium_priority = [n for n in notifications if n.get('priority') == 'medium']
            info_notifications = [n for n in notifications if n.get('priority') == 'info']
            
            # Tampilkan notifikasi penting dulu
            if high_priority:
                console.print("[bold red]🚨 NOTIFIKASI PENTING:[/bold red]")
                for notif in high_priority:
                    message = self.notification_manager.format_notification_message(notif)
                    console.print(f"   {message}")
                console.print("")
            
            if medium_priority:
                console.print("[bold yellow]⚠️  NOTIFIKASI MENENGAH:[/bold yellow]")
                for notif in medium_priority:
                    message = self.notification_manager.format_notification_message(notif)
                    console.print(f"   {message}")
                console.print("")
            
            if info_notifications:
                console.print("[bold blue]ℹ️  INFORMASI:[/bold blue]")
                for notif in info_notifications:
                    message = self.notification_manager.format_notification_message(notif)
                    console.print(f"   {message}")
            
            console.print(f"\n[bold]Total notifikasi: {len(notifications)}[/bold]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def system_summary(self):
        console.clear()
        console.print("[bold cyan]📊 RINGKASAN SISTEM[/bold cyan]")
        console.print("=" * 60)
        
        try:
            # Statistik data
            from models.employee import Employee
            from models.transaction import Transaction
            from models.tax import TaxRecord
            
            employee_count = len(Employee.get_all())
            transaction_count = len(Transaction.get_all())
            tax_record_count = len(TaxRecord.get_all())
            
            console.print("[bold]📊 Statistik Data:[/bold]")
            console.print(f"   Pegawai        : {employee_count} orang")
            console.print(f"   Transaksi      : {transaction_count} transaksi")
            console.print(f"   Catatan Pajak  : {tax_record_count} record")
            
            # Pengaturan aplikasi
            console.print(f"\n[bold]⚙️  Pengaturan Aplikasi:[/bold]")
            console.print(f"   Nama Perusahaan: {self.settings.get('company_name')}")
            console.print(f"   Tarif PPN      : {self.settings.get('ppn_rate')*100:.1f}%")
            console.print(f"   Tarif Pajak    : {self.settings.get('corporate_tax_rate')*100:.1f}%")
            
            # Informasi sistem
            console.print(f"\n[bold]🖥️  Informasi Sistem:[/bold]")
            console.print(f"   Direktori Kerja: {os.getcwd()}")
            console.print(f"   Auto Backup    : {'Aktif' if self.settings.get('auto_backup') else 'Nonaktif'}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def reset_settings(self):
        console.clear()
        console.print("[bold red]⚡ RESET PENGATURAN[/bold red]")
        console.print("=" * 50)
        
        console.print("[bold yellow]⚠️  PERINGATAN: Tindakan ini akan mereset semua pengaturan ke default![/bold yellow]")
        console.print("Data pegawai, transaksi, dan catatan pajak TIDAK akan terhapus.")
        
        confirm = Confirm.ask("\nLanjutkan reset pengaturan?")
        if confirm:
            if self.settings.reset_to_default():
                console.print("[bold green]✅ Pengaturan berhasil direset ke default![/bold green]")
            else:
                console.print("[bold red]❌ Gagal mereset pengaturan![/bold red]")
        else:
            console.print("[yellow]❌ Reset dibatalkan[/yellow]")
        
        input("\nTekan Enter untuk kembali...")