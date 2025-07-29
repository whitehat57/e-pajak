import sqlite3
import os
from typing import Any

class DatabaseManager:
    def __init__(self, db_path: str = "tax_manager.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabel pegawai
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status TEXT NOT NULL, -- tetap/tidak_tetap
                monthly_salary REAL DEFAULT 0,
                allowances REAL DEFAULT 0,
                npwp TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL, -- penjualan/belanja
                description TEXT,
                amount REAL NOT NULL,
                ppn_amount REAL DEFAULT 0,
                transaction_date DATE DEFAULT CURRENT_DATE,
                invoice_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel catatan pajak
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                period TEXT, -- bulan/tahun (format: YYYY-MM atau YYYY)
                gross_income REAL DEFAULT 0,
                taxable_income REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                tax_type TEXT, -- pph21/ppn
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        conn.commit()
        conn.close()

# Inisialisasi database
db_manager = DatabaseManager()