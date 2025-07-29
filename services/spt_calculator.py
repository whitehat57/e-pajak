from typing import List, Dict
from models.employee import Employee
from models.transaction import Transaction
from models.tax import TaxRecord
from services.pp21_calculator import PPh21Calculator
from services.ppn_calculator import PPNCalculator

class SPTCalculator:
    def __init__(self):
        self.pph21_calculator = PPh21Calculator
        self.ppn_calculator = PPNCalculator()
    
    def calculate_annual_income_summary(self, year: int = 2024) -> Dict[str, float]:
        """
        Hitung rekap penghasilan tahunan untuk SPT
        """
        # Ambil semua transaksi untuk tahun tertentu
        all_transactions = Transaction.get_all()
        year_transactions = [t for t in all_transactions if t.transaction_date.startswith(str(year))]
        
        # Hitung total penjualan
        total_sales = sum(t.amount for t in year_transactions if t.type == "penjualan")
        total_sales_ppn = sum(t.ppn_amount for t in year_transactions if t.type == "penjualan")
        
        # Hitung total belanja
        total_purchases = sum(t.amount for t in year_transactions if t.type == "belanja")
        total_purchases_ppn = sum(t.ppn_amount for t in year_transactions if t.type == "belanja")
        
        # Hitung penghasilan bruto
        gross_income = total_sales
        
        # Hitung biaya usaha (bisa dikembangkan lebih lanjut)
        business_expenses = total_purchases  # Asumsi sederhana: semua belanja adalah biaya usaha
        
        # Hitung penghasilan neto
        net_income = gross_income - business_expenses
        
        return {
            'year': year,
            'total_sales': total_sales,
            'total_sales_ppn': total_sales_ppn,
            'total_purchases': total_purchases,
            'total_purchases_ppn': total_purchases_ppn,
            'gross_income': gross_income,
            'business_expenses': business_expenses,
            'net_income': net_income
        }
    
    def calculate_employee_pph21_summary(self, year: int = 2024) -> Dict[str, float]:
        """
        Hitung rekap PPh 21 pegawai untuk SPT
        """
        employees = Employee.get_all()
        total_gross_salary = 0
        total_allowances = 0
        total_pph21 = 0
        
        for employee in employees:
            # Hitung total gaji tahunan
            annual_salary = employee.monthly_salary * 12
            annual_allowances = employee.allowances * 12
            total_gross_salary += annual_salary
            total_allowances += annual_allowances
            
            # Hitung PPh 21 untuk pegawai ini
            calculator = self.pph21_calculator(employee, 0, False)  # Asumsi sederhana
            pph21_result = calculator.calculate_with_npwp_discount()
            total_pph21 += pph21_result['final_tax']
        
        return {
            'year': year,
            'total_employees': len(employees),
            'total_gross_salary': total_gross_salary,
            'total_allowances': total_allowances,
            'total_pph21_withheld': total_pph21
        }
    
    def calculate_ppn_summary(self, year: int = 2024) -> Dict[str, float]:
        """
        Hitung rekap PPN untuk SPT
        """
        all_transactions = Transaction.get_all()
        year_transactions = [t for t in all_transactions if t.transaction_date.startswith(str(year))]
        
        # Gunakan PPN calculator untuk rekap
        ppn_summary = self.ppn_calculator.calculate_monthly_ppn_summary(year_transactions)
        
        return {
            'year': year,
            'total_transactions': ppn_summary['total_transaksi'],
            'ppn_input': ppn_summary['ppn_masukan'],
            'ppn_output': ppn_summary['ppn_keluaran'],
            'ppn_payable': ppn_summary['ppn_terutang']
        }
    
    def generate_spt_annual_report(self, year: int = 2024) -> Dict[str, any]:
        """
        Generate laporan SPT tahunan lengkap
        """
        # Hitung komponen-komponen SPT
        income_summary = self.calculate_annual_income_summary(year)
        employee_summary = self.calculate_employee_pph21_summary(year)
        ppn_summary = self.calculate_ppn_summary(year)
        
        # Hitung pajak terutang
        total_taxable_income = income_summary['net_income']
        # Untuk sederhana, kita asumsikan tarif pajak 25% untuk badan
        corporate_tax_rate = 0.25
        corporate_tax_payable = max(0, total_taxable_income * corporate_tax_rate)
        
        # Hitung pajak yang sudah dibayar (PPh 21 dipotong)
        tax_paid = employee_summary['total_pph21_withheld']
        
        # Hitung pajak terutang bersih
        net_tax_payable = max(0, corporate_tax_payable - tax_paid)
        
        return {
            'year': year,
            'income_summary': income_summary,
            'employee_summary': employee_summary,
            'ppn_summary': ppn_summary,
            'tax_calculation': {
                'taxable_income': total_taxable_income,
                'corporate_tax_rate': corporate_tax_rate,
                'corporate_tax_payable': corporate_tax_payable,
                'tax_paid': tax_paid,
                'net_tax_payable': net_tax_payable
            },
            'generated_at': __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_tax_payment_schedule(self, year: int = 2024) -> List[Dict[str, any]]:
        """
        Dapatkan jadwal pembayaran pajak
        """
        schedule = []
        
        # PPh 21 Bulanan (dibayar oleh pemberi kerja)
        for month in range(1, 13):
            schedule.append({
                'period': f"{year}-{month:02d}",
                'tax_type': 'PPh 21',
                'due_date': f"{year}-{month:02d}-20",  # Tanggal 20 setiap bulan
                'status': 'Dibayar oleh pemberi kerja'
            })
        
        # PPN Bulanan
        for month in range(1, 13):
            schedule.append({
                'period': f"{year}-{month:02d}",
                'tax_type': 'PPN',
                'due_date': f"{year}-{month:02d}-15",  # Tanggal 15 setiap bulan
                'status': 'Harus dilaporkan'
            })
        
        # SPT Tahunan
        schedule.append({
            'period': str(year),
            'tax_type': 'SPT Tahunan',
            'due_date': f"{year+1}-03-31",  # 31 Maret tahun berikutnya
            'status': 'Wajib dilaporkan'
        })
        
        return schedule