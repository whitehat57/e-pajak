from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
import os
from utils.exporter import ReportExporter

console = Console()

class ExportMenu:
    def __init__(self):
        self.exporter = ReportExporter()
    
    def show_export_menu(self):
        while True:
            console.clear()
            console.print("[bold orange]📤 EKSPOR LAPORAN[/bold orange]")
            console.print("=" * 50)
            
            menu_options = [
                "[1] 👥 Ekspor Data Pegawai",
                "[2] 📈 Ekspor Data Transaksi",
                "[3] 💰 Ekspor Data Catatan Pajak",
                "[4] 📊 Ekspor Laporan SPT Tahunan",
                "[5] 📋 Lihat Riwayat Ekspor",
                "[6] 🗑️  Hapus File Ekspor",
                "[0] 🔙 Kembali ke Menu Utama"
            ]
            
            for option in menu_options:
                console.print(option)
            
            console.print("=" * 50)
            choice = Prompt.ask("[bold]Pilih menu[/bold]", choices=["0","1","2","3","4","5","6"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.export_employees()
            elif choice == "2":
                self.export_transactions()
            elif choice == "3":
                self.export_tax_records()
            elif choice == "4":
                self.export_spt_report()
            elif choice == "5":
                self.show_export_history()
            elif choice == "6":
                self.delete_export_file()
    
    def export_employees(self):
        console.clear()
        console.print("[bold blue]👥 EKSPOR DATA PEGAWAI[/bold blue]")
        console.print("=" * 50)
        
        try:
            console.print("Pilih format ekspor:")
            console.print("[1] CSV")
            console.print("[2] Excel")
            format_choice = Prompt.ask("Format", choices=["1","2"])
            
            if format_choice == "1":
                filename = self.exporter.export_employees_to_csv()
                console.print(f"[bold green]✅ Data pegawai berhasil diekspor ke:[/bold green]")
                console.print(f"   {filename}")
            else:
                filename = self.exporter.export_employees_to_excel()
                console.print(f"[bold green]✅ Data pegawai berhasil diekspor ke:[/bold green]")
                console.print(f"   {filename}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def export_transactions(self):
        console.clear()
        console.print("[bold green]📈 EKSPOR DATA TRANSAKSI[/bold green]")
        console.print("=" * 50)
        
        try:
            console.print("Pilih format ekspor:")
            console.print("[1] CSV")
            console.print("[2] Excel")
            format_choice = Prompt.ask("Format", choices=["1","2"])
            
            if format_choice == "1":
                filename = self.exporter.export_transactions_to_csv()
                console.print(f"[bold green]✅ Data transaksi berhasil diekspor ke:[/bold green]")
                console.print(f"   {filename}")
            else:
                filename = self.exporter.export_transactions_to_excel()
                console.print(f"[bold green]✅ Data transaksi berhasil diekspor ke:[/bold green]")
                console.print(f"   {filename}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def export_tax_records(self):
        console.clear()
        console.print("[bold yellow]💰 EKSPOR DATA CATATAN PAJAK[/bold yellow]")
        console.print("=" * 50)
        
        try:
            console.print("Pilih format ekspor:")
            console.print("[1] CSV")
            console.print("[2] Excel")
            format_choice = Prompt.ask("Format", choices=["1","2"])
            
            if format_choice == "1":
                filename = self.exporter.export_tax_records_to_csv()
                console.print(f"[bold green]✅ Data catatan pajak berhasil diekspor ke:[/bold green]")
                console.print(f"   {filename}")
            else:
                filename = self.exporter.export_tax_records_to_excel()
                console.print(f"[bold green]✅ Data catatan pajak berhasil diekspor ke:[/bold green]")
                console.print(f"   {filename}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def export_spt_report(self):
        console.clear()
        console.print("[bold cyan]📊 EKSPOR LAPORAN SPT TAHUNAN[/bold cyan]")
        console.print("=" * 50)
        
        try:
            # Untuk demo, kita buat data SPT sederhana
            # Dalam implementasi sebenarnya, ini akan diambil dari SPT calculator
            from datetime import datetime
            from services.spt_calculator import SPTCalculator
            
            year = Prompt.ask("Tahun pelaporan", default=str(datetime.now().year - 1))
            year = int(year)
            
            # Generate data SPT
            spt_calculator = SPTCalculator()
            spt_data = spt_calculator.generate_spt_annual_report(year)
            
            # Ekspor ke Excel
            filename = self.exporter.export_spt_summary_to_excel(spt_data)
            console.print(f"[bold green]✅ Laporan SPT tahunan berhasil diekspor ke:[/bold green]")
            console.print(f"   {filename}")
            
            console.print(f"\n[bold]Konten Laporan:[/bold]")
            console.print(f"• Ringkasan SPT")
            console.print(f"• Detail Pegawai ({spt_data['employee_summary']['total_employees']} orang)")
            console.print(f"• Detail Transaksi")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_export_history(self):
        console.clear()
        console.print("[bold purple]📋 RIWAYAT EKSPOR[/bold purple]")
        console.print("=" * 80)
        
        try:
            history = self.exporter.get_export_history()
            
            if not history:
                console.print("[yellow]⚠️  Belum ada file ekspor[/yellow]")
                input("\nTekan Enter untuk kembali...")
                return
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("No", style="dim", width=4)
            table.add_column("Nama File", width=30)
            table.add_column("Ukuran", justify="right", width=12)
            table.add_column("Tanggal", width=20)
            
            for i, record in enumerate(history[:20], 1):  # Tampilkan maksimal 20 file terbaru
                # Format ukuran file
                size = record['size']
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                
                table.add_row(
                    str(i),
                    record['filename'],
                    size_str,
                    record['modified']
                )
            
            console.print(table)
            console.print(f"\n[bold]Total file: {len(history)}[/bold]")
            
            # Tampilkan lokasi direktori ekspor
            console.print(f"\n[bold]Lokasi direktori ekspor:[/bold]")
            console.print(f"   {os.path.abspath(self.exporter.export_dir)}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def delete_export_file(self):
        console.clear()
        console.print("[bold red]🗑️  HAPUS FILE EKSPOR[/bold red]")
        console.print("=" * 50)
        
        try:
            history = self.exporter.get_export_history()
            
            if not history:
                console.print("[yellow]⚠️  Belum ada file ekspor[/yellow]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Tampilkan daftar file
            self.show_export_history()
            
            filename = Prompt.ask("\nMasukkan nama file yang akan dihapus")
            
            # Cek apakah file ada
            file_exists = any(record['filename'] == filename for record in history)
            
            if not file_exists:
                console.print("[bold red]❌ File tidak ditemukan![/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Konfirmasi hapus
            confirm = Confirm.ask(f"Yakin ingin menghapus file '{filename}'?")
            if confirm:
                if self.exporter.delete_export_file(filename):
                    console.print("[bold green]✅ File berhasil dihapus![/bold green]")
                else:
                    console.print("[bold red]❌ Gagal menghapus file![/bold red]")
            else:
                console.print("[yellow]❌ Pembatalan penghapusan[/yellow]")
                
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")