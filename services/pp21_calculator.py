from typing import Dict, List
from models.employee import Employee

class PPh21Calculator:
    # PTKP (Penghasilan Tidak Kena Pajak) berdasarkan Excel - Tahun 2024
    # Sumber: Baris 198-201 dan 204-207 di Excel
    PTKP_DIRI_SENDIRI = 54000000  # TK/0 atau K/0
    PTKP_ISTRI = 54000000         # Tambahan untuk K/I/0, K/I/1, K/I/2, K/I/3
    PTKP_ANAK = 4500000           # Per anak, maksimal 3 anak (Baris 197)
    
    # Tarif PPh 21 Progresif Tahunan (berdasarkan UU & PMK terbaru)
    # Sumber: Sheet1, baris 174-178
    TAX_RATES = [
        (60000000, 0.05),    # 5% untuk penghasilan <= 60 juta
        (190000000, 0.15),   # 15% untuk penghasilan >60jt s.d 250 juta
        (250000000, 0.25),   # 25% untuk penghasilan >250jt s.d 500 juta
        (5000000000, 0.30),  # 30% untuk penghasilan >500jt s.d 5 miliar
        (float('inf'), 0.35) # 35% untuk penghasilan > 5 miliar
    ]
    
    # Tarif TER Bulanan (Tarif Efektif Rata-rata) - Kategori A (TK/0, TK/1, TK/2, TK/3)
    # Sumber: Sheet1, baris 117-147
    TER_RATES_A = [
        (5400000, 0.00),      # 0% untuk <= 5.4 juta
        (5650000, 0.0025),    # 0.25% untuk >5.4jt s.d 5.65jt
        (5950000, 0.0050),    # 0.50% untuk >5.65jt s.d 5.95jt
        (6300000, 0.0075),    # 0.75% untuk >5.95jt s.d 6.3jt
        (6750000, 0.0100),    # 1% untuk >6.3jt s.d 6.75jt
        (7500000, 0.0125),    # 1.25% untuk >6.75jt s.d 7.5jt
        (8550000, 0.0150),    # 1.5% untuk >7.5jt s.d 8.55jt
        (9650000, 0.0175),    # 1.75% untuk >8.55jt s.d 9.65jt
        (10050000, 0.0200),   # 2% untuk >9.65jt s.d 10.05jt
        (10350000, 0.0225),   # 2.25% untuk >10.05jt s.d 10.35jt
        (10700000, 0.0250),   # 2.5% untuk >10.35jt s.d 10.7jt
        (11050000, 0.0300),   # 3% untuk >10.7jt s.d 11.05jt
        (11600000, 0.0350),   # 3.5% untuk >11.05jt s.d 11.6jt
        (12500000, 0.0400),   # 4% untuk >11.6jt s.d 12.5jt
        (13750000, 0.0500),   # 5% untuk >12.5jt s.d 13.75jt
        (15100000, 0.0600),   # 6% untuk >13.75jt s.d 15.1jt
        (16950000, 0.0700),   # 7% untuk >15.1jt s.d 16.95jt
        (19750000, 0.0800),   # 8% untuk >16.95jt s.d 19.75jt
        (24150000, 0.0900),   # 9% untuk >19.75jt s.d 24.15jt
        (26450000, 0.1000),   # 10% untuk >24.15jt s.d 26.45jt
        (28000000, 0.1100),   # 11% untuk >26.45jt s.d 28jt
        (30050000, 0.1200),   # 12% untuk >28jt s.d 30.05jt
        (32400000, 0.1300),   # 13% untuk >30.05jt s.d 32.4jt
        (35400000, 0.1400),   # 14% untuk >32.4jt s.d 35.4jt
        (39100000, 0.1500),   # 15% untuk >35.4jt s.d 39.1jt
        (43850000, 0.1600),   # 16% untuk >39.1jt s.d 43.85jt
        (47800000, 0.1700),   # 17% untuk >43.85jt s.d 47.8jt
        (51400000, 0.1800),   # 18% untuk >47.8jt s.d 51.4jt
        (56300000, 0.1900),   # 19% untuk >51.4jt s.d 56.3jt
        (62200000, 0.2000),   # 20% untuk >56.3jt s.d 62.2jt
        (68600000, 0.2100),   # 21% untuk >62.2jt s.d 68.6jt
        (77500000, 0.2200),   # 22% untuk >68.6jt s.d 77.5jt
        (89000000, 0.2300),   # 23% untuk >77.5jt s.d 89jt
        (103000000, 0.2400),  # 24% untuk >89jt s.d 103jt
        (125000000, 0.2500),  # 25% untuk >103jt s.d 125jt
        (157000000, 0.2600),  # 26% untuk >125jt s.d 157jt
        (206000000, 0.2700),  # 27% untuk >157jt s.d 206jt
        (337000000, 0.2800),  # 28% untuk >206jt s.d 337jt
        (454000000, 0.2900),  # 29% untuk >337jt s.d 454jt
        (550000000, 0.3000),  # 30% untuk >454jt s.d 550jt
        (695000000, 0.3100),  # 31% untuk >550jt s.d 695jt
        (910000000, 0.3200),  # 32% untuk >695jt s.d 910jt
        (1400000000, 0.3300), # 33% untuk >910jt s.d 1.4miliar
        (float('inf'), 0.3400) # 34% untuk >1.4miliar
    ]

    # Tarif TER Bulanan - Kategori B (K/0, K/1, K/2, K/3)
    # Sumber: Sheet1, baris 150-171
    TER_RATES_B = [
        (6200000, 0.00),      # 0% untuk <= 6.2 juta
        (6500000, 0.0025),    # 0.25% untuk >6.2jt s.d 6.5jt
        (6850000, 0.0050),    # 0.50% untuk >6.5jt s.d 6.85jt
        (7300000, 0.0075),    # 0.75% untuk >6.85jt s.d 7.3jt
        (9200000, 0.0100),    # 1% untuk >7.3jt s.d 9.2jt
        (10750000, 0.0150),   # 1.5% untuk >9.2jt s.d 10.75jt
        (11250000, 0.0200),   # 2% untuk >10.75jt s.d 11.25jt
        (11600000, 0.0250),   # 2.5% untuk >11.25jt s.d 11.6jt
        (12600000, 0.0300),   # 3% untuk >11.6jt s.d 12.6jt
        (13600000, 0.0400),   # 4% untuk >12.6jt s.d 13.6jt
        (14950000, 0.0500),   # 5% untuk >13.6jt s.d 14.95jt
        (16400000, 0.0600),   # 6% untuk >14.95jt s.d 16.4jt
        (18450000, 0.0700),   # 7% untuk >16.4jt s.d 18.45jt
        (21850000, 0.0800),   # 8% untuk >18.45jt s.d 21.85jt
        (26000000, 0.0900),   # 9% untuk >21.85jt s.d 26jt
        (27700000, 0.1000),   # 10% untuk >26jt s.d 27.7jt
        (29350000, 0.1100),   # 11% untuk >27.7jt s.d 29.35jt
        (31450000, 0.1200),   # 12% untuk >29.35jt s.d 31.45jt
        (33950000, 0.1300),   # 13% untuk >31.45jt s.d 33.95jt
        (37100000, 0.1400),   # 14% untuk >33.95jt s.d 37.1jt
        (41100000, 0.1500),   # 15% untuk >37.1jt s.d 41.1jt
        (45800000, 0.1600),   # 16% untuk >41.1jt s.d 45.8jt
        (49500000, 0.1700),   # 17% untuk >45.8jt s.d 49.5jt
        (53800000, 0.1800),   # 18% untuk >49.5jt s.d 53.8jt
        (58500000, 0.1900),   # 19% untuk >53.8jt s.d 58.5jt
        (64000000, 0.2000),   # 20% untuk >58.5jt s.d 64jt
        (71000000, 0.2100),   # 21% untuk >64jt s.d 71jt
        (80000000, 0.2200),   # 22% untuk >71jt s.d 80jt
        (93000000, 0.2300),   # 23% untuk >80jt s.d 93jt
        (109000000, 0.2400),  # 24% untuk >93jt s.d 109jt
        (129000000, 0.2500),  # 25% untuk >109jt s.d 129jt
        (163000000, 0.2600),  # 26% untuk >129jt s.d 163jt
        (211000000, 0.2700),  # 27% untuk >163jt s.d 211jt
        (374000000, 0.2800),  # 28% untuk >211jt s.d 374jt
        (459000000, 0.2900),  # 29% untuk >374jt s.d 459jt
        (555000000, 0.3000),  # 30% untuk >459jt s.d 555jt
        (704000000, 0.3100),  # 31% untuk >555jt s.d 704jt
        (957000000, 0.3200),  # 32% untuk >704jt s.d 957jt
        (1405000000, 0.3300), # 33% untuk >957jt s.d 1.405miliar
        (float('inf'), 0.3400) # 34% untuk >1.405miliar
    ]

    # Tarif TER Bulanan - Kategori C (K/I/0, K/I/1, K/I/2, K/I/3)
    # Sumber: Sheet1, baris 85-115
    TER_RATES_C = [
        (6600000, 0.00),      # 0% untuk <= 6.6 juta
        (6950000, 0.0025),    # 0.25% untuk >6.6jt s.d 6.95jt
        (7350000, 0.0050),    # 0.50% untuk >6.95jt s.d 7.35jt
        (7800000, 0.0075),    # 0.75% untuk >7.35jt s.d 7.8jt
        (8850000, 0.0100),    # 1% untuk >7.8jt s.d 8.85jt
        (9800000, 0.0125),    # 1.25% untuk >8.85jt s.d 9.8jt
        (10950000, 0.0200),   # 2% untuk >9.8jt s.d 10.95jt
        (11200000, 0.0175),   # 1.75% untuk >10.95jt s.d 11.2jt
        (12050000, 0.0200),   # 2% untuk >11.2jt s.d 12.05jt
        (12950000, 0.0300),   # 3% untuk >12.05jt s.d 12.95jt
        (14150000, 0.0400),   # 4% untuk >12.95jt s.d 14.15jt
        (15550000, 0.0500),   # 5% untuk >14.15jt s.d 15.55jt
        (17050000, 0.0600),   # 6% untuk >15.55jt s.d 17.05jt
        (19500000, 0.0700),   # 7% untuk >17.05jt s.d 19.5jt
        (22700000, 0.0800),   # 8% untuk >19.5jt s.d 22.7jt
        (26600000, 0.0900),   # 9% untuk >22.7jt s.d 26.6jt
        (28100000, 0.1000),   # 10% untuk >26.6jt s.d 28.1jt
        (30100000, 0.1100),   # 11% untuk >28.1jt s.d 30.1jt
        (32600000, 0.1200),   # 12% untuk >30.1jt s.d 32.6jt
        (35400000, 0.1300),   # 13% untuk >32.6jt s.d 35.4jt
        (38900000, 0.1400),   # 14% untuk >35.4jt s.d 38.9jt
        (43000000, 0.1500),   # 15% untuk >38.9jt s.d 43jt
        (47400000, 0.1600),   # 16% untuk >43jt s.d 47.4jt
        (51200000, 0.1700),   # 17% untuk >47.4jt s.d 51.2jt
        (55800000, 0.1800),   # 18% untuk >51.2jt s.d 55.8jt
        (60400000, 0.1900),   # 19% untuk >55.8jt s.d 60.4jt
        (66700000, 0.2000),   # 20% untuk >60.4jt s.d 66.7jt
        (74500000, 0.2100),   # 21% untuk >66.7jt s.d 74.5jt
        (83200000, 0.2200),   # 22% untuk >74.5jt s.d 83.2jt
        (95600000, 0.2300),   # 23% untuk >83.2jt s.d 95.6jt
        (110000000, 0.2400),  # 24% untuk >95.6jt s.d 110jt
        (134000000, 0.2500),  # 25% untuk >110jt s.d 134jt
        (169000000, 0.2600),  # 26% untuk >134jt s.d 169jt
        (221000000, 0.2700),  # 27% untuk >169jt s.d 221jt
        (390000000, 0.2800),  # 28% untuk >221jt s.d 390jt
        (463000000, 0.2900),  # 29% untuk >390jt s.d 463jt
        (561000000, 0.3000),  # 30% untuk >463jt s.d 561jt
        (709000000, 0.3100),  # 31% untuk >561jt s.d 709jt
        (965000000, 0.3200),  # 32% untuk >709jt s.d 965jt
        (1419000000, 0.3300), # 33% untuk >965jt s.d 1.419miliar
        (float('inf'), 0.3400) # 34% untuk >1.419miliar
    ]

    def __init__(self, employee: Employee, num_children: int = 0, has_spouse: bool = False, joint_filing: bool = False):
        self.employee = employee
        self.num_children = min(num_children, 3)  # Maksimal 3 anak (Baris 197)
        self.has_spouse = has_spouse
        self.joint_filing = joint_filing # K/I/ status
        
    def calculate_ptkp(self) -> float:
        """Hitung total PTKP berdasarkan status"""
        # Sumber: Baris 198-207 di Excel
        if self.joint_filing: # K/I/0, K/I/1, K/I/2, K/I/3
            total_ptkp = self.PTKP_DIRI_SENDIRI + self.PTKP_ISTRI
        elif self.has_spouse: # K/0, K/1, K/2, K/3
            total_ptkp = self.PTKP_DIRI_SENDIRI + self.PTKP_ISTRI
        else: # TK/0, TK/1, TK/2, TK/3
            total_ptkp = self.PTKP_DIRI_SENDIRI
            
        total_ptkp += self.PTKP_ANAK * self.num_children
        return total_ptkp
    
    def calculate_gross_annual_income(self) -> float:
        """Hitung penghasilan bruto tahunan"""
        monthly_income = self.employee.monthly_salary + self.employee.allowances
        return monthly_income * 12
    
    def calculate_taxable_income(self) -> float:
        """Hitung penghasilan kena pajak (PKP)"""
        gross_income = self.calculate_gross_annual_income()
        ptkp = self.calculate_ptkp()
        
        # Biaya jabatan: 5% dari bruto, maksimal Rp 6.000.000 per tahun
        # Sumber: Catatan di baris 25 di Excel
        biaya_jabatan = min(gross_income * 0.05, 6000000)
        net_income = gross_income - biaya_jabatan
        
        pkp = max(0, net_income - ptkp)
        return pkp, gross_income, net_income, biaya_jabatan, ptkp
    
    def calculate_pph21_tax_progressive(self) -> Dict[str, float]:
        """Hitung PPh 21 terutang dengan tarif progresif"""
        pkp, gross_income, net_income, biaya_jabatan, ptkp = self.calculate_taxable_income()
        
        if pkp <= 0:
            return {
                'gross_income': gross_income,
                'biaya_jabatan': biaya_jabatan,
                'net_income': net_income,
                'ptkp': ptkp,
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
                'bracket_limit': bracket_limit,
                'rate': rate,
                'taxable_amount': taxable_in_bracket,
                'tax': tax_in_bracket
            })
            
            if bracket_limit == float('inf'):
                break
        
        monthly_tax = tax_amount / 12
        
        return {
            'gross_income': gross_income,
            'biaya_jabatan': biaya_jabatan,
            'net_income': net_income,
            'ptkp': ptkp,
            'taxable_income': pkp,
            'tax_amount': tax_amount,
            'monthly_tax': monthly_tax,
            'breakdown': tax_breakdown
        }
    
    def calculate_pph21_tax_ter(self) -> Dict[str, float]:
        """Hitung PPh 21 terutang dengan Tarif Efektif Rata-rata (TER)"""
        gross_income = self.calculate_gross_annual_income()
        monthly_gross = gross_income / 12
        
        # Tentukan kategori TER berdasarkan status
        if self.joint_filing: # K/I/0, K/I/1, K/I/2, K/I/3
            ter_rates = self.TER_RATES_C
        elif self.has_spouse: # K/0, K/1, K/2, K/3
            ter_rates = self.TER_RATES_B
        else: # TK/0, TK/1, TK/2, TK/3
            ter_rates = self.TER_RATES_A
            
        # Cari tarif efektif berdasarkan penghasilan bulanan
        effective_rate = 0.0
        for limit, rate in ter_rates:
            if monthly_gross <= limit:
                effective_rate = rate
                break
        else:
            # Jika penghasilan melebihi batas tertinggi
            effective_rate = ter_rates[-1][1] if ter_rates else 0.0
        
        tax_amount = gross_income * effective_rate
        monthly_tax = tax_amount / 12
        
        # Hitung komponen lain untuk konsistensi dengan metode progresif
        ptkp = self.calculate_ptkp()
        biaya_jabatan = min(gross_income * 0.05, 6000000)
        net_income = gross_income - biaya_jabatan
        pkp = max(0, net_income - ptkp)
        
        return {
            'gross_income': gross_income,
            'biaya_jabatan': biaya_jabatan,
            'net_income': net_income,
            'ptkp': ptkp,
            'taxable_income': pkp,
            'tax_amount': tax_amount,
            'monthly_tax': monthly_tax,
            'effective_rate': effective_rate,
            'method': 'TER'
        }
    
    def calculate_with_npwp_discount(self, use_ter: bool = False) -> Dict[str, float]:
        """Hitung PPh 21 dengan diskon 5% untuk yang memiliki NPWP"""
        if use_ter:
            result = self.calculate_pph21_tax_ter()
        else:
            result = self.calculate_pph21_tax_progressive()
            
        if self.employee.npwp:
            result['discount'] = result['tax_amount'] * 0.05
            result['final_tax'] = result['tax_amount'] - result['discount']
            result['monthly_final_tax'] = result['final_tax'] / 12
        else:
            result['discount'] = 0
            result['final_tax'] = result['tax_amount']
            result['monthly_final_tax'] = result['tax_amount'] / 12
            
        result['use_ter'] = use_ter
        return result