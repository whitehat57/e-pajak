import pandas as pd
import csv
from datetime import datetime
from typing import List, Dict
from models.employee import Employee
from models.transaction import Transaction
from models.tax import TaxRecord
import os

class ReportExporter:
    def __init__(self):
        # Buat direktori export jika belum ada
        self.export_dir = "exports"
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_employees_to_csv(self) -> str:
        """Ekspor data pegawai ke CSV"""
        employees = Employee.get_all()
        
        if not employees:
            raise Exception("Tidak ada data pegawai untuk diekspor")
        
        # Siapkan data untuk export
        data = []
        for emp in employees:
            data.append({
                'ID': emp.id,
                'Nama': emp.name,
                'Status': emp.status,
                'Gaji_Bulanan': emp.monthly_salary,
                'Tunjangan': emp.allowances,
                'NPWP': emp.npwp or '',
                'Tanggal_Dibuat': emp.created_at
            })
        
        # Buat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_dir}/pegawai_{timestamp}.csv"
        
        # Ekspor ke CSV
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return filename
    
    def export_employees_to_excel(self) -> str:
        """Ekspor data pegawai ke Excel"""
        employees = Employee.get_all()
        
        if not employees:
            raise Exception("Tidak ada data pegawai untuk diekspor")
        
        # Siapkan data untuk export
        data = []
        for emp in employees:
            data.append({
                'ID': emp.id,
                'Nama': emp.name,
                'Status': emp.status.title(),
                'Gaji Bulanan': emp.monthly_salary,
                'Tunjangan': emp.allowances,
                'NPWP': emp.npwp or '-',
                'Tanggal Dibuat': emp.created_at
            })
        
        # Buat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_dir}/pegawai_{timestamp}.xlsx"
        
        # Ekspor ke Excel
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, sheet_name='Data Pegawai')
        
        return filename
    
    def export_transactions_to_csv(self) -> str:
        """Ekspor data transaksi ke CSV"""
        transactions = Transaction.get_all()
        
        if not transactions:
            raise Exception("Tidak ada data transaksi untuk diekspor")
        
        # Siapkan data untuk export
        data = []
        for trans in transactions:
            total_amount = trans.amount + trans.ppn_amount
            data.append({
                'ID': trans.id,
                'Jenis': trans.type,
                'Deskripsi': trans.description,
                'Jumlah': trans.amount,
                'PPN': trans.ppn_amount,
                'Total': total_amount,
                'Tanggal': trans.transaction_date,
                'No_Faktur': trans.invoice_number or '',
                'Tanggal_Dibuat': trans.created_at
            })
        
        # Buat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_dir}/transaksi_{timestamp}.csv"
        
        # Ekspor ke CSV
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return filename
    
    def export_transactions_to_excel(self) -> str:
        """Ekspor data transaksi ke Excel"""
        transactions = Transaction.get_all()
        
        if not transactions:
            raise Exception("Tidak ada data transaksi untuk diekspor")
        
        # Siapkan data untuk export
        data = []
        for trans in transactions:
            total_amount = trans.amount + trans.ppn_amount
            data.append({
                'ID': trans.id,
                'Jenis': trans.type.title(),
                'Deskripsi': trans.description,
                'Jumlah': trans.amount,
                'PPN': trans.ppn_amount,
                'Total': total_amount,
                'Tanggal': trans.transaction_date,
                'No. Faktur': trans.invoice_number or '-',
                'Tanggal Dibuat': trans.created_at
            })
        
        # Buat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_dir}/transaksi_{timestamp}.xlsx"
        
        # Ekspor ke Excel
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, sheet_name='Data Transaksi')
        
        return filename
    
    def export_tax_records_to_csv(self) -> str:
        """Ekspor data catatan pajak ke CSV"""
        tax_records = TaxRecord.get_all()
        
        if not tax_records:
            raise Exception("Tidak ada data catatan pajak untuk diekspor")
        
        # Siapkan data untuk export
        data = []
        for record in tax_records:
            # Dapatkan nama pegawai jika ada
            employee_name = "-"
            if record.employee_id:
                employee = Employee.get_by_id(record.employee_id)
                if employee:
                    employee_name = employee.name
            
            data.append({
                'ID': record.id,
                'Nama_Pegawai': employee_name,
                'Periode': record.period,
                'Jenis_Pajak': record.tax_type,
                'Penghasilan_Bruto': record.gross_income,
                'PKP': record.taxable_income,
                'Pajak_Terutang': record.tax_amount,
                'Deskripsi': record.description,
                'Tanggal_Dibuat': record.created_at
            })
        
        # Buat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_dir}/catatan_pajak_{timestamp}.csv"
        
        # Ekspor ke CSV
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return filename
    
    def export_tax_records_to_excel(self) -> str:
        """Ekspor data catatan pajak ke Excel"""
        tax_records = TaxRecord.get_all()
        
        if not tax_records:
            raise Exception("Tidak ada data catatan pajak untuk diekspor")
        
        # Siapkan data untuk export
        data = []
        for record in tax_records:
            # Dapatkan nama pegawai jika ada
            employee_name = "-"
            if record.employee_id:
                employee = Employee.get_by_id(record.employee_id)
                if employee:
                    employee_name = employee.name
            
            data.append({
                'ID': record.id,
                'Nama Pegawai': employee_name,
                'Periode': record.period,
                'Jenis Pajak': record.tax_type.upper(),
                'Penghasilan Bruto': record.gross_income,
                'PKP': record.taxable_income,
                'Pajak Terutang': record.tax_amount,
                'Deskripsi': record.description,
                'Tanggal Dibuat': record.created_at
            })
        
        # Buat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_dir}/catatan_pajak_{timestamp}.xlsx"
        
        # Ekspor ke Excel
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, sheet_name='Catatan Pajak')
        
        return filename
    
    def export_spt_summary_to_excel(self, spt_data: Dict) -> str:
        """Ekspor ringkasan SPT ke Excel dengan multiple sheet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_dir}/spt_tahunan_{spt_data['year']}_{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Ringkasan SPT
            summary_data = {
                'Komponen': [
                    'Tahun Pelaporan',
                    'Total Penjualan',
                    'PPN Keluaran',
                    'Total Pembelian',
                    'PPN Masukan',
                    'Penghasilan Bruto',
                    'Biaya Usaha',
                    'Penghasilan Neto',
                    'Jumlah Pegawai',
                    'Total Gaji Pokok',
                    'Total Tunjangan',
                    'PPh 21 Dipotong',
                    'PPN Terutang',
                    'Penghasilan Kena Pajak',
                    'PPh Badan Terutang',
                    'PPh 21 Telah Dibayar',
                    'PPh Badan Terutang Bersih'
                ],
                'Nilai': [
                    spt_data['year'],
                    spt_data['income_summary']['total_sales'],
                    spt_data['income_summary']['total_sales_ppn'],
                    spt_data['income_summary']['total_purchases'],
                    spt_data['income_summary']['total_purchases_ppn'],
                    spt_data['income_summary']['gross_income'],
                    spt_data['income_summary']['business_expenses'],
                    spt_data['income_summary']['net_income'],
                    spt_data['employee_summary']['total_employees'],
                    spt_data['employee_summary']['total_gross_salary'],
                    spt_data['employee_summary']['total_allowances'],
                    spt_data['employee_summary']['total_pph21_withheld'],
                    spt_data['ppn_summary']['ppn_payable'],
                    spt_data['tax_calculation']['taxable_income'],
                    spt_data['tax_calculation']['corporate_tax_payable'],
                    spt_data['tax_calculation']['tax_paid'],
                    spt_data['tax_calculation']['net_tax_payable']
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Ringkasan SPT', index=False)
            
            # Sheet 2: Detail Pegawai
            employees = Employee.get_all()
            if employees:
                employee_data = []
                for emp in employees:
                    employee_data.append({
                        'ID': emp.id,
                        'Nama': emp.name,
                        'Status': emp.status.title(),
                        'Gaji Bulanan': emp.monthly_salary,
                        'Tunjangan Bulanan': emp.allowances,
                        'Gaji Tahunan': (emp.monthly_salary + emp.allowances) * 12,
                        'NPWP': emp.npwp or '-'
                    })
                
                employee_df = pd.DataFrame(employee_data)
                employee_df.to_excel(writer, sheet_name='Detail Pegawai', index=False)
            
            # Sheet 3: Detail Transaksi
            transactions = Transaction.get_all()
            if transactions:
                transaction_data = []
                for trans in transactions:
                    transaction_data.append({
                        'Tanggal': trans.transaction_date,
                        'Jenis': trans.type.title(),
                        'Deskripsi': trans.description,
                        'Jumlah': trans.amount,
                        'PPN': trans.ppn_amount,
                        'Total': trans.amount + trans.ppn_amount,
                        'No. Faktur': trans.invoice_number or '-'
                    })
                
                transaction_df = pd.DataFrame(transaction_data)
                transaction_df.to_excel(writer, sheet_name='Detail Transaksi', index=False)
        
        return filename
    
    def get_export_history(self) -> List[Dict]:
        """Dapatkan riwayat ekspor file"""
        history = []
        
        if os.path.exists(self.export_dir):
            for filename in os.listdir(self.export_dir):
                if filename.endswith(('.csv', '.xlsx')):
                    file_path = os.path.join(self.export_dir, filename)
                    file_stat = os.stat(file_path)
                    history.append({
                        'filename': filename,
                        'filepath': file_path,
                        'size': file_stat.st_size,
                        'modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        # Urutkan berdasarkan tanggal modifikasi (terbaru dulu)
        history.sort(key=lambda x: x['modified'], reverse=True)
        return history
    
    def delete_export_file(self, filename: str) -> bool:
        """Hapus file ekspor"""
        file_path = os.path.join(self.export_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False