from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import print as rprint
from datetime import datetime
from services.spt_calculator import SPTCalculator

console = Console()

class SPTMenu:
    def __init__(self):
        self.spt_calculator = SPTCalculator()
    
    def show_spt_menu(self):
        while True:
            console.clear()
            console.print("[bold cyan]📊 LAPORAN SPT TAHUNAN[/bold cyan]")
            console.print("=" * 50)
            
            menu_options = [
                "[1] 📋 Lihat Laporan SPT Tahunan",
                "[2] 📊 Rekap Penghasilan Usaha",
                "[3] 👥 Rekap PPh 21 Pegawai",
                "[4] 📦 Rekap PPN",
                "[5] 📅 Jadwal Pembayaran Pajak",
                "[6] 📤 Ekspor Laporan SPT",
                "[0] 🔙 Kembali ke Menu Utama"
            ]
            
            for option in menu_options:
                console.print(option)
            
            console.print("=" * 50)
            choice = Prompt.ask("[bold]Pilih menu[/bold]", choices=["0","1","2","3","4","5","6"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.show_annual_spt_report()
            elif choice == "2":
                self.show_income_summary()
            elif choice == "3":
                self.show_employee_tax_summary()
            elif choice == "4":
                self.show_ppn_summary()
            elif choice == "5":
                self.show_tax_schedule()
            elif choice == "6":
                self.export_spt_report()
    
    def show_annual_spt_report(self):
        console.clear()
        console.print("[bold blue]📋 LAPORAN SPT TAHUNAN LENGKAP[/bold blue]")
        console.print("=" * 80)
        
        try:
            year = IntPrompt.ask("Tahun pelaporan", default=datetime.now().year - 1)
            report = self.spt_calculator.generate_spt_annual_report(year)
            
            # Header laporan
            console.print(Panel(f"[bold]LAPORAN SPT TAHUNAN {year}[/bold]", expand=False))
            console.print(f"Dibuat pada: {report['generated_at']}")
            console.print("=" * 80)
            
            # Section 1: Ringkasan Penghasilan
            console.print("\n[bold underline]1. RINGKASAN PENGHASILAN[/bold underline]")
            income = report['income_summary']
            table1 = Table(show_header=False, box=None)
            table1.add_row("Total Penjualan", f"Rp {income['total_sales']:,.0f}")
            table1.add_row("PPN Keluaran", f"Rp {income['total_sales_ppn']:,.0f}")
            table1.add_row("Total Pembelian", f"Rp {income['total_purchases']:,.0f}")
            table1.add_row("PPN Masukan", f"Rp {income['total_purchases_ppn']:,.0f}")
            table1.add_row("[bold]Penghasilan Bruto[/bold]", f"[bold]Rp {income['gross_income']:,.0f}[/bold]")
            table1.add_row("Biaya Usaha", f"Rp {income['business_expenses']:,.0f}")
            table1.add_row("[bold]Penghasilan Neto[/bold]", f"[bold]Rp {income['net_income']:,.0f}[/bold]")
            console.print(table1)
            
            # Section 2: Rekap PPh 21 Pegawai
            console.print("\n[bold underline]2. REKAP PPH 21 PEGAWAI[/bold underline]")
            employee = report['employee_summary']
            table2 = Table(show_header=False, box=None)
            table2.add_row("Jumlah Pegawai", f"{employee['total_employees']} orang")
            table2.add_row("Total Gaji Pokok", f"Rp {employee['total_gross_salary']:,.0f}")
            table2.add_row("Total Tunjangan", f"Rp {employee['total_allowances']:,.0f}")
            table2.add_row("[bold]PPh 21 Dipotong[/bold]", f"[bold]Rp {employee['total_pph21_withheld']:,.0f}[/bold]")
            console.print(table2)
            
            # Section 3: Rekap PPN
            console.print("\n[bold underline]3. REKAP PPN[/bold underline]")
            ppn = report['ppn_summary']
            table3 = Table(show_header=False, box=None)
            table3.add_row("Total Transaksi", f"Rp {ppn['total_transactions']:,.0f}")
            table3.add_row("PPN Masukan", f"Rp {ppn['ppn_input']:,.0f}")
            table3.add_row("PPN Keluaran", f"Rp {ppn['ppn_output']:,.0f}")
            table3.add_row("[bold]PPN Terutang[/bold]", f"[bold]Rp {ppn['ppn_payable']:,.0f}[/bold]")
            console.print(table3)
            
            # Section 4: Perhitungan Pajak Terutang
            console.print("\n[bold underline]4. PERHITUNGAN PAJAK TERUTANG[/bold underline]")
            tax = report['tax_calculation']
            table4 = Table(show_header=False, box=None)
            table4.add_row("Penghasilan Kena Pajak", f"Rp {tax['taxable_income']:,.0f}")
            table4.add_row("Tarif Pajak Badan", f"{tax['corporate_tax_rate']*100:.0f}%")
            table4.add_row("PPh Badan Terutang", f"Rp {tax['corporate_tax_payable']:,.0f}")
            table4.add_row("PPh 21 Telah Dibayar", f"Rp {tax['tax_paid']:,.0f}")
            table4.add_row("[bold green]PPh Badan Terutang Bersih[/bold green]", f"[bold green]Rp {tax['net_tax_payable']:,.0f}[/bold green]")
            console.print(table4)
            
            # Kesimpulan
            console.print(f"\n[bold green]📝 KESIMPULAN:[/bold green]")
            if tax['net_tax_payable'] > 0:
                console.print(f"   Anda harus membayar PPh Badan sebesar [bold]Rp {tax['net_tax_payable']:,.0f}[/bold]")
            else:
                console.print(f"   Anda memiliki kelebihan pembayaran pajak sebesar [bold]Rp {abs(tax['net_tax_payable']):,.0f}[/bold]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_income_summary(self):
        console.clear()
        console.print("[bold yellow]📊 REKAP PENGHASILAN USAHA[/bold yellow]")
        console.print("=" * 70)
        
        try:
            year = IntPrompt.ask("Tahun", default=datetime.now().year - 1)
            summary = self.spt_calculator.calculate_annual_income_summary(year)
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Komponen", width=25)
            table.add_column("Jumlah", justify="right")
            
            table.add_row("Total Penjualan", f"Rp {summary['total_sales']:,.0f}")
            table.add_row("PPN Keluaran", f"Rp {summary['total_sales_ppn']:,.0f}")
            table.add_row("Total Pembelian", f"Rp {summary['total_purchases']:,.0f}")
            table.add_row("PPN Masukan", f"Rp {summary['total_purchases_ppn']:,.0f}")
            table.add_row("[bold]Penghasilan Bruto[/bold]", f"[bold]Rp {summary['gross_income']:,.0f}[/bold]")
            table.add_row("Biaya Usaha", f"Rp {summary['business_expenses']:,.0f}")
            table.add_row("[bold green]Penghasilan Neto[/bold green]", f"[bold green]Rp {summary['net_income']:,.0f}[/bold green]")
            
            console.print(table)
            
            # Tampilkan grafik sederhana
            if summary['gross_income'] > 0:
                profit_margin = (summary['net_income'] / summary['gross_income'] * 100) if summary['gross_income'] > 0 else 0
                console.print(f"\n[bold]Margin Keuntungan: {profit_margin:.1f}%[/bold]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_employee_tax_summary(self):
        console.clear()
        console.print("[bold magenta]👥 REKAP PPH 21 PEGAWAI[/bold magenta]")
        console.print("=" * 70)
        
        try:
            year = IntPrompt.ask("Tahun", default=datetime.now().year - 1)
            summary = self.spt_calculator.calculate_employee_pph21_summary(year)
            
            console.print(f"\n[bold]Ringkasan Tahun {year}:[/bold]")
            console.print("-" * 40)
            console.print(f"Jumlah Pegawai        : {summary['total_employees']} orang")
            console.print(f"Total Gaji Pokok      : Rp {summary['total_gross_salary']:,.0f}")
            console.print(f"Total Tunjangan       : Rp {summary['total_allowances']:,.0f}")
            console.print(f"[bold]Total PPh 21 Dipotong : Rp {summary['total_pph21_withheld']:,.0f}[/bold]")
            
            # Detail per pegawai
            from models.employee import Employee
            employees = Employee.get_all()
            
            if employees:
                console.print(f"\n[bold underline]Detail Per Pegawai:[/bold underline]")
                table = Table(show_header=True, header_style="bold green")
                table.add_column("Nama", width=20)
                table.add_column("Status", width=12)
                table.add_column("Gaji/Tahun", justify="right")
                table.add_column("PPh 21/Tahun", justify="right")
                
                for emp in employees:
                    calculator = self.spt_calculator.pph21_calculator(emp, 0, False)
                    pph21_result = calculator.calculate_with_npwp_discount()
                    
                    table.add_row(
                        emp.name,
                        emp.status.title(),
                        f"Rp {((emp.monthly_salary + emp.allowances) * 12):,.0f}",
                        f"Rp {pph21_result['final_tax']:,.0f}"
                    )
                
                console.print(table)
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_ppn_summary(self):
        console.clear()
        console.print("[bold orange]📦 REKAP PPN[/bold orange]")
        console.print("=" * 70)
        
        try:
            year = IntPrompt.ask("Tahun", default=datetime.now().year - 1)
            summary = self.spt_calculator.calculate_ppn_summary(year)
            
            table = Table(show_header=True, header_style="bold purple")
            table.add_column("Komponen", width=20)
            table.add_column("Jumlah", justify="right")
            
            table.add_row("Total Transaksi", f"Rp {summary['total_transactions']:,.0f}")
            table.add_row("PPN Masukan", f"Rp {summary['ppn_input']:,.0f}")
            table.add_row("PPN Keluaran", f"Rp {summary['ppn_output']:,.0f}")
            table.add_row("[bold]PPN Terutang[/bold]", f"[bold]Rp {summary['ppn_payable']:,.0f}[/bold]")
            
            console.print(table)
            
            # Analisis PPN
            console.print(f"\n[bold]Analisis PPN:[/bold]")
            if summary['ppn_payable'] > 0:
                console.print(f"   🔸 Anda harus membayar PPN sebesar Rp {summary['ppn_payable']:,.0f}")
            elif summary['ppn_payable'] < 0:
                console.print(f"   🔸 Anda memiliki kelebihan PPN sebesar Rp {abs(summary['ppn_payable']):,.0f}")
                console.print(f"      (dapat dikreditkan atau dikembalikan)")
            else:
                console.print(f"   🔸 PPN seimbang (tidak ada kewajiban)")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_tax_schedule(self):
        console.clear()
        console.print("[bold green]📅 JADWAL PEMBAYARAN PAJAK[/bold green]")
        console.print("=" * 80)
        
        try:
            year = IntPrompt.ask("Tahun", default=datetime.now().year)
            schedule = self.spt_calculator.get_tax_payment_schedule(year)
            
            # Kelompokkan berdasarkan jenis pajak
            pph21_schedule = [s for s in schedule if s['tax_type'] == 'PPh 21']
            ppn_schedule = [s for s in schedule if s['tax_type'] == 'PPN']
            spt_schedule = [s for s in schedule if s['tax_type'] == 'SPT Tahunan']
            
            # Tampilkan PPh 21 Bulanan
            console.print(f"\n[bold underline]PPh 21 Bulanan (Dibayar oleh pemberi kerja):[/bold underline]")
            table1 = Table(show_header=True, header_style="bold blue")
            table1.add_column("Bulan", width=10)
            table1.add_column("Jatuh Tempo", width=12)
            table1.add_column("Status", width=25)
            
            for item in pph21_schedule:
                table1.add_row(
                    item['period'][5:],  # Hanya bulan
                    item['due_date'][8:],  # Hanya tanggal
                    item['status']
                )
            
            console.print(table1)
            
            # Tampilkan PPN Bulanan
            console.print(f"\n[bold underline]PPN Bulanan:[/bold underline]")
            table2 = Table(show_header=True, header_style="bold yellow")
            table2.add_column("Bulan", width=10)
            table2.add_column("Jatuh Tempo", width=12)
            table2.add_column("Status", width=25)
            
            for item in ppn_schedule:
                table2.add_row(
                    item['period'][5:],  # Hanya bulan
                    item['due_date'][8:],  # Hanya tanggal
                    item['status']
                )
            
            console.print(table2)
            
            # Tampilkan SPT Tahunan
            console.print(f"\n[bold underline]SPT Tahunan:[/bold underline]")
            table3 = Table(show_header=True, header_style="bold red")
            table3.add_column("Periode", width=15)
            table3.add_column("Jatuh Tempo", width=15)
            table3.add_column("Status", width=30)
            
            for item in spt_schedule:
                table3.add_row(
                    item['period'],
                    item['due_date'],
                    item['status']
                )
            
            console.print(table3)
            
            # Peringatan penting
            console.print(f"\n[bold yellow]⚠️  PERINGATAN PENTING:[/bold yellow]")
            console.print(f"   • Keterlambatan pembayaran dikenakan bunga 2% per bulan")
            console.print(f"   • Keterlambatan pelaporan dikenakan sanksi administratif")
            console.print(f"   • Pastikan selalu menyimpan bukti pembayaran")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def export_spt_report(self):
        console.clear()
        console.print("[bold purple]📤 EKSPOR LAPORAN SPT[/bold purple]")
        console.print("=" * 50)
        
        console.print("[yellow]Fitur ekspor laporan SPT akan diimplementasikan pada bagian ekspor laporan.[/yellow]")
        console.print("Anda dapat mengekspor laporan SPT melalui menu [7] 📤 Ekspor Laporan")
        
        input("\nTekan Enter untuk kembali...")