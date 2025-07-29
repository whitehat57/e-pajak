from typing import Dict, List
from models.employee import Employee

class PPh21Calculator:
    # PTKP (Penghasilan Tidak Kena Pajak) 2024
    PTKP_DIRI_SENDIRI = 54000000
    PTKP_Istri = 54000000
    PTKP_ANAK = 54000000  # per anak maksimal 3
    
    # Tarif PPh 21 Progresif
    TAX_RATES = [
        (50000000, 0.05),   # 5% untuk penghasilan <= 50 juta
        (250000000, 0.15),  # 15% untuk penghasilan 50-300 juta
        (500000000, 0.25),  # 25% untuk penghasilan 300-800 juta
        (5000000000, 0.30), # 30% untuk penghasilan 800jt-5miliar
        (float('inf'), 0.35) # 35% untuk penghasilan > 5 miliar
    ]
    
    def __init__(self, employee: Employee, num_children: int = 0, has_spouse: bool = False):
        self.employee = employee
        self.num_children = min(num_children, 3)  # maksimal 3 anak
        self.has_spouse = has_spouse
    
    def calculate_ptkp(self) -> float:
        """Hitung total PTKP"""
        total_ptkp = self.PTKP_DIRI_SENDIRI
        if self.has_spouse:
            total_ptkp += self.PTKP_Istri
        total_ptkp += self.PTKP_ANAK * self.num_children
        return total_ptkp
    
    def calculate_gross_annual_income(self) -> float:
        """Hitung penghasilan bruto tahunan"""
        # Untuk pegawai tetap: gaji pokok + tunjangan
        # Untuk pegawai tidak tetap: dihitung dari data tersedia
        monthly_income = self.employee.monthly_salary + self.employee.allowances
        return monthly_income * 12
    
    def calculate_taxable_income(self) -> float:
        """Hitung penghasilan kena pajak (PKP)"""
        gross_income = self.calculate_gross_annual_income()
        ptkp = self.calculate_ptkp()
        pkp = max(0, gross_income - ptkp)
        return pkp
    
    def calculate_pph21_tax(self) -> Dict[str, float]:
        """Hitung PPh 21 terutang"""
        pkp = self.calculate_taxable_income()
        
        if pkp <= 0:
            return {
                'gross_income': self.calculate_gross_annual_income(),
                'ptkp': self.calculate_ptkp(),
                'taxable_income': 0,
                'tax_amount': 0,
                'monthly_tax': 0
            }
        
        tax_amount = 0
        remaining_pkp = pkp
        tax_breakdown = []
        
        for bracket_limit, rate in self.TAX_RATES:
            if remaining_pkp <= 0:
                break
                
            taxable_in_bracket = min(remaining_pkp, bracket_limit)
            tax_in_bracket = taxable_in_bracket * rate
            tax_amount += tax_in_bracket
            remaining_pkp -= taxable_in_bracket
            
            tax_breakdown.append({
                'bracket': f"s.d {bracket_limit:,}",
                'rate': rate,
                'taxable_amount': taxable_in_bracket,
                'tax': tax_in_bracket
            })
            
            if bracket_limit == float('inf'):
                break
        
        monthly_tax = tax_amount / 12
        
        return {
            'gross_income': self.calculate_gross_annual_income(),
            'ptkp': self.calculate_ptkp(),
            'taxable_income': pkp,
            'tax_amount': tax_amount,
            'monthly_tax': monthly_tax,
            'breakdown': tax_breakdown
        }
    
    def calculate_with_npwp_discount(self) -> Dict[str, float]:
        """Hitung PPh 21 dengan diskon 5% untuk yang memiliki NPWP"""
        result = self.calculate_pph21_tax()
        if self.employee.npwp:
            result['discount'] = result['tax_amount'] * 0.05
            result['final_tax'] = result['tax_amount'] - result['discount']
            result['monthly_final_tax'] = result['final_tax'] / 12
        else:
            result['discount'] = 0
            result['final_tax'] = result['tax_amount']
            result['monthly_final_tax'] = result['tax_amount'] / 12
        return result

# Perbaikan agar bisa diakses sebagai class method dari SPT
pph21_calculator = PPh21Calculator