from dataclasses import dataclass
from typing import Optional
import sqlite3
from config.database import db_manager

@dataclass
class TaxRecord:
    id: Optional[int] = None
    employee_id: Optional[int] = None
    period: str = ""  # format: YYYY-MM atau YYYY
    gross_income: float = 0.0
    taxable_income: float = 0.0
    tax_amount: float = 0.0
    tax_type: str = "pph21"  # pph21/ppn
    description: str = ""
    
    def save(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO tax_records 
                (employee_id, period, gross_income, taxable_income, tax_amount, tax_type, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.employee_id, self.period, self.gross_income, self.taxable_income, 
                  self.tax_amount, self.tax_type, self.description))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE tax_records 
                SET employee_id=?, period=?, gross_income=?, taxable_income=?, 
                    tax_amount=?, tax_type=?, description=?
                WHERE id=?
            ''', (self.employee_id, self.period, self.gross_income, self.taxable_income,
                  self.tax_amount, self.tax_type, self.description, self.id))
        
        conn.commit()
        conn.close()
    
    @classmethod
    def get_all(cls):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tax_records')
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_by_employee(cls, employee_id: int):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tax_records WHERE employee_id=? ORDER BY period DESC', (employee_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_by_period(cls, period: str):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tax_records WHERE period=?', (period,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]