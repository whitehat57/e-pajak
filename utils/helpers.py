from datetime import datetime
import os

def format_currency(amount: float) -> str:
    """Format angka ke format mata uang Rupiah"""
    return f"Rp {amount:,.0f}"

def format_percentage(value: float) -> str:
    """Format angka ke format persentase"""
    return f"{value*100:.1f}%"

def get_current_year() -> int:
    """Dapatkan tahun saat ini"""
    return datetime.now().year

def get_current_month() -> str:
    """Dapatkan bulan saat ini dalam format YYYY-MM"""
    return datetime.now().strftime("%Y-%m")

def create_directory_if_not_exists(directory: str) -> None:
    """Buat direktori jika belum ada"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def validate_year(year: str) -> bool:
    """Validasi format tahun"""
    try:
        year_int = int(year)
        current_year = datetime.now().year
        return 2000 <= year_int <= current_year + 1
    except ValueError:
        return False

def validate_date(date_str: str) -> bool:
    """Validasi format tanggal YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False