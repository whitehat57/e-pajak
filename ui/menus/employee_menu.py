from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich import print as rprint
from datetime import datetime
from models.employee import Employee
from models.tax import TaxRecord
from services.pp21_calculator import PPh21Calculator

console = Console()

class EmployeeMenu:
    def __init__(self):
        pass
    
    def show_employee_menu(self):
        while True:
            console.clear()
            console.print("[bold blue]👥 KELOLA PEGAWAI[/bold blue]")
            console.print("=" * 50)
            
            menu_options = [
                "[1] 📋 Lihat Daftar Pegawai",
                "[2] ➕ Tambah Pegawai Baru",
                "[3] ✏️  Edit Data Pegawai",
                "[4] 🗑️  Hapus Pegawai",
                "[5] 💰 Hitung PPh 21",
                "[6] 📊 Lihat Riwayat Pajak Pegawai",
                "[0] 🔙 Kembali ke Menu Utama"
            ]
            
            for option in menu_options:
                console.print(option)
            
            console.print("=" * 50)
            choice = Prompt.ask("[bold]Pilih menu[/bold]", choices=["0","1","2","3","4","5","6"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.list_employees()
            elif choice == "2":
                self.add_employee()
            elif choice == "3":
                self.edit_employee()
            elif choice == "4":
                self.delete_employee()
            elif choice == "5":
                self.calculate_pph21()
            elif choice == "6":
                self.view_tax_history()
    
    def list_employees(self):
        console.clear()
        console.print("[bold cyan]📋 DAFTAR PEGAWAI[/bold cyan]")
        console.print("=" * 80)
        
        employees = Employee.get_all()
        
        if not employees:
            console.print("[yellow]⚠️  Belum ada data pegawai[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("Nama", width=25)
        table.add_column("Status", width=12)
        table.add_column("Gaji Bulanan", justify="right")
        table.add_column("Tunjangan", justify="right")
        table.add_column("NPWP", width=15)
        table.add_column("Tgl Dibuat", width=12)
        
        for emp in employees:
            table.add_row(
                str(emp.id),
                emp.name,
                emp.status.title(),
                f"Rp {emp.monthly_salary:,.0f}",
                f"Rp {emp.allowances:,.0f}",
                emp.npwp or "-",
                emp.created_at[:10] if emp.created_at else "-"
            )
        
        console.print(table)
        input("\nTekan Enter untuk kembali...")
    
    def add_employee(self):
        console.clear()
        console.print("[bold green]➕ TAMBAH PEGAWAI BARU[/bold green]")
        console.print("=" * 50)
        
        try:
            name = Prompt.ask("Nama lengkap pegawai")
            status = Prompt.ask("Status kepegawaian", choices=["tetap", "tidak_tetap"], default="tetap")
            monthly_salary = FloatPrompt.ask("Gaji pokok bulanan (Rp)")
            allowances = FloatPrompt.ask("Tunjangan bulanan (Rp)", default=0.0)
            npwp = Prompt.ask("Nomor NPWP (opsional)", default="")
            
            if not npwp:
                npwp = None
            
            employee = Employee(
                name=name,
                status=status,
                monthly_salary=monthly_salary,
                allowances=allowances,
                npwp=npwp
            )
            employee.save()
            
            console.print("[bold green]✅ Pegawai berhasil ditambahkan![/bold green]")
            console.print(f"ID Pegawai: {employee.id}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def edit_employee(self):
        console.clear()
        console.print("[bold yellow]✏️  EDIT DATA PEGAWAI[/bold yellow]")
        console.print("=" * 50)
        
        employees = Employee.get_all()
        if not employees:
            console.print("[yellow]⚠️  Belum ada data pegawai[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        # Tampilkan daftar pegawai
        self.list_employees()
        
        try:
            emp_id = IntPrompt.ask("\nMasukkan ID pegawai yang akan diedit")
            employee = Employee.get_by_id(emp_id)
            
            if not employee or employee.id is None:
                console.print("[bold red]❌ Pegawai tidak ditemukan![/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            console.print(f"\n[bold]Mengedit  {employee.name}[/bold]")
            console.print("-" * 30)
            
            # Input data baru
            name = Prompt.ask("Nama lengkap pegawai", default=employee.name)
            status = Prompt.ask("Status kepegawaian", choices=["tetap", "tidak_tetap"], default=employee.status)
            monthly_salary = FloatPrompt.ask("Gaji pokok bulanan (Rp)", default=employee.monthly_salary)
            allowances = FloatPrompt.ask("Tunjangan bulanan (Rp)", default=employee.allowances)
            npwp = Prompt.ask("Nomor NPWP (opsional)", default=employee.npwp or "")
            
            if not npwp:
                npwp = None
            
            # Update data
            employee.name = name
            employee.status = status
            employee.monthly_salary = monthly_salary
            employee.allowances = allowances
            employee.npwp = npwp
            employee.save()
            
            console.print("[bold green]✅ Data pegawai berhasil diperbarui![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def delete_employee(self):
        console.clear()
        console.print("[bold red]🗑️  HAPUS PEGAWAI[/bold red]")
        console.print("=" * 50)
        
        employees = Employee.get_all()
        if not employees:
            console.print("[yellow]⚠️  Belum ada data pegawai[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        # Tampilkan daftar pegawai
        self.list_employees()
        
        try:
            emp_id = IntPrompt.ask("\nMasukkan ID pegawai yang akan dihapus")
            employee = Employee.get_by_id(emp_id)
            
            if not employee or employee.id is None:
                console.print("[bold red]❌ Pegawai tidak ditemukan![/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Tampilkan detail pegawai
            console.print(f"\n[bold]Detail Pegawai:[/bold]")
            console.print(f"Nama        : {employee.name}")
            console.print(f"Status      : {employee.status.title()}")
            console.print(f"Gaji Bulanan: Rp {employee.monthly_salary:,.0f}")
            console.print(f"Tunjangan   : Rp {employee.allowances:,.0f}")
            
            # Konfirmasi hapus
            confirm = Confirm.ask(f"\nYakin ingin menghapus pegawai '{employee.name}'?")
            if confirm:
                employee.delete()
                console.print("[bold green]✅ Pegawai berhasil dihapus![/bold green]")
            else:
                console.print("[yellow]❌ Pembatalan penghapusan[/yellow]")
                
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def calculate_pph21(self):
        console.clear()
        console.print("[bold yellow]💰 HITUNG PPH 21[/bold yellow]")
        console.print("=" * 50)
        
        employees = Employee.get_all()
        if not employees:
            console.print("[yellow]⚠️  Belum ada data pegawai[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        # Tampilkan daftar pegawai
        self.list_employees()
        
        try:
            emp_id = IntPrompt.ask("\nMasukkan ID pegawai untuk perhitungan PPh 21")
            employee = Employee.get_by_id(emp_id)
            
            if not employee or employee.id is None:
                console.print("[bold red]❌ Pegawai tidak ditemukan![/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            console.print(f"\n[bold]Perhitungan PPh 21 untuk: {employee.name}[/bold]")
            console.print("-" * 50)
            
            # Input data tambahan untuk perhitungan
            status_kawin = Prompt.ask("Status kawin", choices=["TK", "K", "K/I"], default="TK")
            jumlah_tanggungan = IntPrompt.ask("Jumlah tanggungan (maksimal 3)", default=0, choices=["0","1","2","3"])
            
            # Tentukan status pernikahan dan joint filing
            has_spouse = status_kawin in ["K", "K/I"]
            joint_filing = status_kawin == "K/I"
            
            # Pilihan metode perhitungan
            use_ter = Confirm.ask("Gunakan metode Tarif Efektif Rata-rata (TER)?", default=False)
            
            # Hitung PPh 21
            calculator = PPh21Calculator(employee, jumlah_tanggungan, has_spouse, joint_filing)
            result = calculator.calculate_with_npwp_discount(use_ter)
            
            # Tampilkan hasil perhitungan
            self.display_pph21_result(employee, result, status_kawin, jumlah_tanggungan)
            
            # Simpan ke riwayat pajak
            save_record = Confirm.ask("\nSimpan hasil perhitungan ke riwayat pajak?", default=True)
            if save_record:
                tax_record = TaxRecord()
                tax_record.employee_id = employee.id
                tax_record.period = datetime.now().strftime("%Y")
                tax_record.gross_income = result['gross_income']
                tax_record.taxable_income = result['taxable_income']
                tax_record.tax_amount = result['final_tax']
                tax_record.tax_type = "pph21"
                tax_record.description = f"PPh 21 {status_kawin}/{jumlah_tanggungan} {datetime.now().year}"
                tax_record.save()
                console.print("[bold green]✅ Hasil perhitungan disimpan![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")

    def display_pph21_result(self, employee, result, status_kawin, jumlah_tanggungan):
        console.print(f"\n[bold cyan]📋 HASIL PERHITUNGAN PPH 21[/bold cyan]")
        console.print("=" * 60)
        console.print(f"Nama Pegawai     : {employee.name}")
        console.print(f"Status           : {status_kawin}/{jumlah_tanggungan}")
        console.print(f"NPWP             : {'Ada' if employee.npwp else 'Tidak Ada'}")
        console.print("-" * 60)
        console.print(f"Penghasilan Bruto Tahunan : Rp {result['gross_income']:,.0f}")
        console.print(f"Biaya Jabatan             : Rp {result['biaya_jabatan']:,.0f}")
        console.print(f"Penghasilan Netto         : Rp {result['net_income']:,.0f}")
        console.print(f"PTKP                      : Rp {result['ptkp']:,.0f}")
        console.print(f"Penghasilan Kena Pajak    : Rp {result['taxable_income']:,.0f}")
        
        if result.get('use_ter', False):
            console.print(f"Tarif Efektif             : {result.get('effective_rate', 0)*100:.2f}%")
            console.print(f"PPh 21 Terutang           : Rp {result['tax_amount']:,.0f}")
        else:
            console.print(f"PPh 21 Terutang           : Rp {result['tax_amount']:,.0f}")
        
        if result['discount'] > 0:
            console.print(f"Diskon NPWP (5%)          : Rp {result['discount']:,.0f}")
            console.print(f"[bold]PPh 21 Setelah Diskon        : Rp {result['final_tax']:,.0f}[/bold]")
        
        console.print(f"[bold green]PPh 21 Per Bulan           : Rp {result['monthly_final_tax']:,.0f}[/bold green]")
        
        # Tampilkan breakdown perhitungan (hanya untuk metode progresif)
        if not result.get('use_ter', False) and 'breakdown' in result and result['breakdown']:
            console.print(f"\n[bold]🧮 Breakdown Perhitungan:[/bold]")
            for bracket in result['breakdown']:
                console.print(f"  • {bracket['rate']*100:,.1f}% dari Rp {bracket['taxable_amount']:,.0f} = Rp {bracket['tax']:,.0f}")

    def view_tax_history(self):
        console.clear()
        console.print("[bold cyan]📊 RIWAYAT PAJAK PEGAWAI[/bold cyan]")
        console.print("=" * 80)
        
        employees = Employee.get_all()
        if not employees:
            console.print("[yellow]⚠️  Belum ada data pegawai[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        # Tampilkan daftar pegawai
        self.list_employees()
        
        try:
            emp_id = IntPrompt.ask("\nMasukkan ID pegawai untuk melihat riwayat pajak")
            employee = Employee.get_by_id(emp_id)
            
            if not employee or employee.id is None:
                console.print("[bold red]❌ Pegawai tidak ditemukan![/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            console.print(f"\n[bold]Riwayat Pajak: {employee.name}[/bold]")
            console.print("-" * 80)
            
            # Ambil riwayat pajak
            tax_records = TaxRecord.get_by_employee(emp_id)
            
            if not tax_records:
                console.print("[yellow]⚠️  Belum ada riwayat perhitungan pajak[/yellow]")
                input("\nTekan Enter untuk kembali...")
                return
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("ID", width=4)
            table.add_column("Periode", width=10)
            table.add_column("Jenis", width=8)
            table.add_column("Bruto", justify="right")
            table.add_column("PKP", justify="right")
            table.add_column("Pajak", justify="right")
            table.add_column("Deskripsi", width=25)
            table.add_column("Tgl Hitung", width=12)
            
            total_tax = 0
            for record in tax_records:
                table.add_row(
                    str(record.id),
                    record.period,
                    record.tax_type.upper(),
                    f"Rp {record.gross_income:,.0f}",
                    f"Rp {record.taxable_income:,.0f}",
                    f"Rp {record.tax_amount:,.0f}",
                    record.description[:25],
                    record.created_at[:10] if record.created_at else "-"
                )
                total_tax += record.tax_amount
            
            console.print(table)
            console.print(f"\n[bold green]Total Pajak Terutang: Rp {total_tax:,.0f}[/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")