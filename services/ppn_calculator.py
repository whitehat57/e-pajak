from typing import List, Dict
from models.transaction import Transaction

class PPNCalculator:
    # Tarif PPN standar Indonesia (2024)
    PPN_RATE = 0.11  # 11%
    
    def __init__(self):
        pass
    
    def calculate_ppn_from_amount(self, amount: float) -> Dict[str, float]:
        """
        Hitung PPN dari jumlah transaksi
        """
        ppn_amount = amount * self.PPN_RATE
        total_amount = amount + ppn_amount
        
        return {
            'base_amount': amount,
            'ppn_amount': ppn_amount,
            'total_amount': total_amount,
            'ppn_rate': self.PPN_RATE
        }
    
    def calculate_base_amount_from_total(self, total_amount: float) -> Dict[str, float]:
        """
        Hitung jumlah dasar dari total (digunakan untuk faktur masukan)
        """
        base_amount = total_amount / (1 + self.PPN_RATE)
        ppn_amount = total_amount - base_amount
        
        return {
            'base_amount': base_amount,
            'ppn_amount': ppn_amount,
            'total_amount': total_amount,
            'ppn_rate': self.PPN_RATE
        }
    
    def calculate_monthly_ppn_summary(self, transactions: List[Transaction], month: str = None) -> Dict[str, float]:
        """
        Hitung rekap PPN bulanan
        """
        ppn_masukan = 0.0
        ppn_keluaran = 0.0
        total_transaksi = 0.0
        
        for transaction in transactions:
            # Filter berdasarkan bulan jika diperlukan
            if month and not transaction.transaction_date.startswith(month):
                continue
                
            if transaction.type == "penjualan":
                ppn_keluaran += transaction.ppn_amount
            elif transaction.type == "belanja":
                ppn_masukan += transaction.ppn_amount
            
            total_transaksi += transaction.amount
        
        ppn_terutang = ppn_keluaran - ppn_masukan
        
        return {
            'total_transaksi': total_transaksi,
            'ppn_masukan': ppn_masukan,
            'ppn_keluaran': ppn_keluaran,
            'ppn_terutang': ppn_terutang,
            'month': month
        }
    
    def calculate_ppn_credit_eligibility(self, transaction: Transaction) -> bool:
        """
        Cek apakah transaksi memenuhi syarat untuk dikreditkan (PPN Masukan)
        """
        # Syarat dasar: harus ada nomor faktur pajak
        if not transaction.invoice_number:
            return False
        
        # Syarat dasar: harus transaksi belanja
        if transaction.type != "belanja":
            return False
        
        # Syarat dasar: harus ada jumlah PPN
        if transaction.ppn_amount <= 0:
            return False
        
        # Bisa ditambahkan syarat lain sesuai ketentuan perpajakan
        return True