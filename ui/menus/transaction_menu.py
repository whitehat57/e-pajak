from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, Confirm
from rich import print as rprint
from datetime import datetime
from models.transaction import Transaction
from services.ppn_calculator import PPNCalculator

console = Console()

class TransactionMenu:
    def __init__(self):
        self.ppn_calculator = PPNCalculator()
    
    def show_transaction_menu(self):
        while True:
            console.clear()
            console.print("[bold green]📈 CATAT TRANSAKSI[/bold green]")
            console.print("=" * 50)
            
            menu_options = [
                "[1] 📋 Lihat Daftar Transaksi",
                "[2] ➕ Catat Transaksi Penjualan",
                "[3] 🛒 Catat Transaksi Belanja",
                "[4] ✏️  Edit Transaksi",
                "[5] 🗑️  Hapus Transaksi",
                "[6] 📊 Rekap PPN Bulanan",
                "[7] 📋 Lihat Faktur Pajak",
                "[0] 🔙 Kembali ke Menu Utama"
            ]
            
            for option in menu_options:
                console.print(option)
            
            console.print("=" * 50)
            choice = Prompt.ask("[bold]Pilih menu[/bold]", choices=["0","1","2","3","4","5","6","7"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.list_transactions()
            elif choice == "2":
                self.record_sale_transaction()
            elif choice == "3":
                self.record_purchase_transaction()
            elif choice == "4":
                self.edit_transaction()
            elif choice == "5":
                self.delete_transaction()
            elif choice == "6":
                self.show_ppn_summary()
            elif choice == "7":
                self.view_tax_invoices()
    
    def list_transactions(self):
        console.clear()
        console.print("[bold cyan]📋 DAFTAR TRANSAKSI[/bold cyan]")
        console.print("=" * 100)
        
        transactions = Transaction.get_all()
        
        if not transactions:
            console.print("[yellow]⚠️  Belum ada data transaksi[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("Tanggal", width=12)
        table.add_column("Jenis", width=12)
        table.add_column("Deskripsi", width=25)
        table.add_column("Jumlah", justify="right")
        table.add_column("PPN", justify="right")
        table.add_column("Total", justify="right")
        table.add_column("No. Faktur", width=15)
        
        total_amount = 0
        total_ppn = 0
        
        for trans in transactions:
            total_with_ppn = trans.amount + trans.ppn_amount
            table.add_row(
                str(trans.id),
                trans.transaction_date,
                trans.type.title(),
                trans.description[:25],
                f"Rp {trans.amount:,.0f}",
                f"Rp {trans.ppn_amount:,.0f}",
                f"Rp {total_with_ppn:,.0f}",
                trans.invoice_number or "-"
            )
            total_amount += trans.amount
            total_ppn += trans.ppn_amount
        
        console.print(table)
        console.print(f"\n[bold]Total Transaksi: Rp {total_amount:,.0f}[/bold]")
        console.print(f"[bold]Total PPN: Rp {total_ppn:,.0f}[/bold]")
        input("\nTekan Enter untuk kembali...")
    
    def record_sale_transaction(self):
        console.clear()
        console.print("[bold yellow]➕ CATAT TRANSAKSI PENJUALAN[/bold yellow]")
        console.print("=" * 50)
        
        try:
            description = Prompt.ask("Deskripsi transaksi")
            amount = FloatPrompt.ask("Jumlah penjualan (sebelum PPN)")
            invoice_number = Prompt.ask("Nomor faktur pajak (opsional)", default="")
            
            if not invoice_number:
                invoice_number = None
            
            # Hitung PPN
            ppn_result = self.ppn_calculator.calculate_ppn_from_amount(amount)
            
            console.print(f"\n[bold cyan]Perhitungan PPN:[/bold cyan]")
            console.print(f"Jumlah Dasar     : Rp {ppn_result['base_amount']:,.0f}")
            console.print(f"PPN ({ppn_result['ppn_rate']*100:.0f}%)       : Rp {ppn_result['ppn_amount']:,.0f}")
            console.print(f"Total            : Rp {ppn_result['total_amount']:,.0f}")
            
            # Konfirmasi simpan
            confirm = Confirm.ask("\nSimpan transaksi penjualan?", default=True)
            if confirm:
                transaction = Transaction(
                    type="penjualan",
                    description=description,
                    amount=ppn_result['base_amount'],
                    ppn_amount=ppn_result['ppn_amount'],
                    transaction_date=datetime.now().strftime("%Y-%m-%d"),
                    invoice_number=invoice_number
                )
                transaction.save()
                
                console.print("[bold green]✅ Transaksi penjualan berhasil dicatat![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def record_purchase_transaction(self):
        console.clear()
        console.print("[bold blue]🛒 CATAT TRANSAKSI BELANJA[/bold blue]")
        console.print("=" * 50)
        
        try:
            description = Prompt.ask("Deskripsi transaksi")
            total_amount = FloatPrompt.ask("Total pembayaran (termasuk PPN)")
            invoice_number = Prompt.ask("Nomor faktur pajak", default="")
            
            if not invoice_number:
                console.print("[yellow]⚠️  Transaksi tanpa nomor faktur tidak dapat dikreditkan![/yellow]")
                invoice_number = None
            
            # Hitung jumlah dasar dan PPN dari total
            ppn_result = self.ppn_calculator.calculate_base_amount_from_total(total_amount)
            
            console.print(f"\n[bold cyan]Perhitungan PPN:[/bold cyan]")
            console.print(f"Jumlah Dasar     : Rp {ppn_result['base_amount']:,.0f}")
            console.print(f"PPN ({ppn_result['ppn_rate']*100:.0f}%)       : Rp {ppn_result['ppn_amount']:,.0f}")
            console.print(f"Total            : Rp {ppn_result['total_amount']:,.0f}")
            
            # Cek kelayakan kredit PPN
            temp_transaction = Transaction(
                type="belanja",
                description=description,
                amount=ppn_result['base_amount'],
                ppn_amount=ppn_result['ppn_amount'],
                transaction_date=datetime.now().strftime("%Y-%m-%d"),
                invoice_number=invoice_number
            )
            
            if self.ppn_calculator.calculate_ppn_credit_eligibility(temp_transaction):
                console.print("[bold green]✅ Transaksi memenuhi syarat untuk dikreditkan![/bold green]")
            else:
                console.print("[yellow]⚠️  Transaksi tidak memenuhi syarat untuk dikreditkan[/yellow]")
            
            # Konfirmasi simpan
            confirm = Confirm.ask("\nSimpan transaksi belanja?", default=True)
            if confirm:
                transaction = temp_transaction
                transaction.save()
                
                console.print("[bold green]✅ Transaksi belanja berhasil dicatat![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def edit_transaction(self):
        console.clear()
        console.print("[bold yellow]✏️  EDIT TRANSAKSI[/bold yellow]")
        console.print("=" * 50)
        
        transactions = Transaction.get_all()
        if not transactions:
            console.print("[yellow]⚠️  Belum ada data transaksi[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        # Tampilkan daftar transaksi
        self.list_transactions()
        
        try:
            trans_id = Prompt.ask("\nMasukkan ID transaksi yang akan diedit")
            transaction = Transaction.get_by_id(trans_id)
            
            if not transaction:
                console.print("[bold red]❌ Transaksi tidak ditemukan![/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            console.print(f"\n[bold]Mengedit transaksi ID: {transaction.id}[/bold]")
            console.print("-" * 30)
            
            # Input data baru
            description = Prompt.ask("Deskripsi transaksi", default=transaction.description)
            amount = FloatPrompt.ask("Jumlah dasar", default=transaction.amount)
            ppn_amount = FloatPrompt.ask("Jumlah PPN", default=transaction.ppn_amount)
            invoice_number = Prompt.ask("Nomor faktur pajak", default=transaction.invoice_number or "")
            
            if not invoice_number:
                invoice_number = None
            
            # Update data
            transaction.description = description
            transaction.amount = amount
            transaction.ppn_amount = ppn_amount
            transaction.invoice_number = invoice_number
            transaction.save()
            
            console.print("[bold green]✅ Data transaksi berhasil diperbarui![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def delete_transaction(self):
        console.clear()
        console.print("[bold red]🗑️  HAPUS TRANSAKSI[/bold red]")
        console.print("=" * 50)
        
        transactions = Transaction.get_all()
        if not transactions:
            console.print("[yellow]⚠️  Belum ada data transaksi[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        # Tampilkan daftar transaksi
        self.list_transactions()
        
        try:
            trans_id = Prompt.ask("\nMasukkan ID transaksi yang akan dihapus")
            transaction = Transaction.get_by_id(trans_id)
            
            if not transaction:
                console.print("[bold red]❌ Transaksi tidak ditemukan![/bold red]")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Tampilkan detail transaksi
            console.print(f"\n[bold]Detail Transaksi:[/bold]")
            console.print(f"Jenis        : {transaction.type.title()}")
            console.print(f"Deskripsi    : {transaction.description}")
            console.print(f"Jumlah       : Rp {transaction.amount:,.0f}")
            console.print(f"PPN          : Rp {transaction.ppn_amount:,.0f}")
            console.print(f"Tanggal      : {transaction.transaction_date}")
            console.print(f"No. Faktur   : {transaction.invoice_number or '-'}")
            
            # Konfirmasi hapus
            confirm = Confirm.ask(f"\nYakin ingin menghapus transaksi ini?")
            if confirm:
                transaction.delete()
                console.print("[bold green]✅ Transaksi berhasil dihapus![/bold green]")
            else:
                console.print("[yellow]❌ Pembatalan penghapusan[/yellow]")
                
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\nTekan Enter untuk kembali...")
    
    def show_ppn_summary(self):
        console.clear()
        console.print("[bold cyan]📊 REKAP PPN BULANAN[/bold cyan]")
        console.print("=" * 70)
        
        transactions = Transaction.get_all()
        if not transactions:
            console.print("[yellow]⚠️  Belum ada data transaksi[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        # Hitung rekap PPN
        ppn_summary = self.ppn_calculator.calculate_monthly_ppn_summary(transactions)
        
        console.print(f"\n[bold]REKAP PPN KESELURUHAN[/bold]")
        console.print("-" * 50)
        console.print(f"Total Transaksi      : Rp {ppn_summary['total_transaksi']:,.0f}")
        console.print(f"PPN Masukan (Kredit) : Rp {ppn_summary['ppn_masukan']:,.0f}")
        console.print(f"PPN Keluaran (Debit) : Rp {ppn_summary['ppn_keluaran']:,.0f}")
        console.print(f"[bold]PPN Terutang         : Rp {ppn_summary['ppn_terutang']:,.0f}[/bold]")
        
        # Tampilkan rekap per bulan
        console.print(f"\n[bold]REKAP PER BULAN:[/bold]")
        monthly_data = {}
        
        for trans in transactions:
            month_key = trans.transaction_date[:7]  # YYYY-MM
            if month_key not in monthly_data:
                monthly_data[month_key] = []
            monthly_data[month_key].append(trans)
        
        if monthly_data:
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Bulan", width=10)
            table.add_column("Transaksi", justify="right")
            table.add_column("PPN Masuk", justify="right")
            table.add_column("PPN Keluar", justify="right")
            table.add_column("PPN Terutang", justify="right")
            
            for month, trans_list in sorted(monthly_data.items()):
                month_summary = self.ppn_calculator.calculate_monthly_ppn_summary(trans_list, month)
                table.add_row(
                    month,
                    f"Rp {month_summary['total_transaksi']:,.0f}",
                    f"Rp {month_summary['ppn_masukan']:,.0f}",
                    f"Rp {month_summary['ppn_keluaran']:,.0f}",
                    f"Rp {month_summary['ppn_terutang']:,.0f}"
                )
            
            console.print(table)
        
        input("\nTekan Enter untuk kembali...")
    
    def view_tax_invoices(self):
        console.clear()
        console.print("[bold purple]📋 DAFTAR FAKTUR PAJAK[/bold purple]")
        console.print("=" * 80)
        
        # Filter transaksi yang memiliki nomor faktur
        all_transactions = Transaction.get_all()
        tax_invoices = [t for t in all_transactions if t.invoice_number]
        
        if not tax_invoices:
            console.print("[yellow]⚠️  Belum ada faktur pajak[/yellow]")
            input("\nTekan Enter untuk kembali...")
            return
        
        table = Table(show_header=True, header_style="bold green")
        table.add_column("No. Faktur", width=18)
        table.add_column("Tanggal", width=12)
        table.add_column("Jenis", width=12)
        table.add_column("Deskripsi", width=25)
        table.add_column("Jumlah", justify="right")
        table.add_column("PPN", justify="right")
        
        for trans in tax_invoices:
            table.add_row(
                trans.invoice_number,
                trans.transaction_date,
                trans.type.title(),
                trans.description[:25],
                f"Rp {trans.amount:,.0f}",
                f"Rp {trans.ppn_amount:,.0f}"
            )
        
        console.print(table)
        console.print(f"\n[bold]Total Faktur Pajak: {len(tax_invoices)}[/bold]")
        input("\nTekan Enter untuk kembali...")