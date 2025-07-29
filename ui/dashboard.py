from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import print as rprint
import os
from ui.menus.employee_menu import EmployeeMenu
from ui.menus.transaction_menu import TransactionMenu
from ui.menus.spt_menu import SPTMenu

console = Console()

class TaxDashboard:
    def __init__(self):
        self.running = True
        self.employee_menu = EmployeeMenu()
        self.transaction_menu = TransactionMenu()
        self.spt_menu = SPTMenu()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_main_menu(self):
        self.clear_screen()
        console.print(Panel.fit("[bold blue]🏢 APLIKASI KELOLA PAJAK USAHA[/bold blue]", border_style="blue"))
        
        table = Table(show_header=False, box=None, padding=(1, 2))
        table.add_column("Menu", style="cyan")
        table.add_column("Deskripsi", style="white")
        
        menu_items = [
            ("[1] 💰 Hitung PPh 21", "Perhitungan pajak penghasilan pegawai"),
            ("[2] 📦 Hitung PPN", "Perhitungan pajak pertambahan nilai"),
            ("[3] 📊 Laporan SPT", "Laporan Surat Pemberitahuan Tahunan"),
            ("[4] 👥 Kelola Pegawai", "Manajemen data pegawai"),
            ("[5] 📈 Catat Transaksi", "Pencatatan transaksi keuangan"),
            ("[6] 📋 Data Master", "Konfigurasi data master"),
            ("[7] 📤 Ekspor Laporan", "Ekspor data ke CSV/Excel"),
            ("[8] ⚙️  Pengaturan", "Pengaturan aplikasi"),
            ("[9] ❌ Keluar", "Keluar dari aplikasi")
        ]
        
        for item, desc in menu_items:
            table.add_row(item, desc)
        
        console.print(table)
        console.print("\n" + "="*80)
    
    def handle_menu_choice(self, choice: str):
        if choice == "1":
            self.employee_menu.calculate_pph21()
        elif choice == "2":
            self.calculate_ppn()
        elif choice == "3":
            self.spt_menu.show_spt_menu()
        elif choice == "4":
            self.employee_menu.show_employee_menu()
        elif choice == "5":
            self.transaction_menu.show_transaction_menu()
        elif choice == "6":
            self.show_master_data()
        elif choice == "7":
            self.export_reports()
        elif choice == "8":
            self.show_settings()
        elif choice == "9":
            self.running = False
            console.print("[bold green]👋 Terima kasih telah menggunakan aplikasi![/bold green]")
        else:
            console.print("[bold red]❌ Pilihan tidak valid![/bold red]")
            input("Tekan Enter untuk melanjutkan...")
    
    def calculate_ppn(self):
        self.clear_screen()
        console.print(Panel("[bold magenta]📦 PERHITUNGAN PPN[/bold magenta]", border_style="magenta"))
        
        # Placeholder untuk implementasi perhitungan PPN
        console.print("Fitur perhitungan PPN akan diimplementasikan...")
        input("\nTekan Enter untuk kembali ke menu utama...")
    
    def show_master_data(self):
        self.clear_screen()
        console.print(Panel("[bold purple]📋 DATA MASTER[/bold purple]", border_style="purple"))
        
        # Placeholder untuk data master
        console.print("Fitur data master akan diimplementasikan...")
        input("\nTekan Enter untuk kembali ke menu utama...")
    
    def export_reports(self):
        self.clear_screen()
        console.print(Panel("[bold orange]📤 EKSPOR LAPORAN[/bold orange]", border_style="orange"))
        
        # Placeholder untuk ekspor laporan
        console.print("Fitur ekspor laporan akan diimplementasikan...")
        input("\nTekan Enter untuk kembali ke menu utama...")
    
    def show_settings(self):
        self.clear_screen()
        console.print(Panel("[bold gray]⚙️  PENGATURAN[/bold gray]", border_style="gray"))
        
        # Placeholder untuk pengaturan
        console.print("Fitur pengaturan akan diimplementasikan...")
        input("\nTekan Enter untuk kembali ke menu utama...")
    
    def run(self):
        while self.running:
            self.show_main_menu()
            choice = Prompt.ask("[bold]Pilih menu[/bold]", choices=["1","2","3","4","5","6","7","8","9"])
            self.handle_menu_choice(choice)

# Jalankan dashboard jika file ini dijalankan langsung
if __name__ == "__main__":
    dashboard = TaxDashboard()
    dashboard.run()