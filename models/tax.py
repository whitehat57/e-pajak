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
    created_at: Optional[str] = None
    
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
        cursor.execute('SELECT id, employee_id, period, gross_income, taxable_income, tax_amount, tax_type, description, created_at FROM tax_records')
        rows = cursor.fetchall()
        conn.close()
        
        tax_records = []
        for row in rows:
            record = cls()
            record.id = row[0]
            record.employee_id = row[1]
            record.period = row[2]
            record.gross_income = row[3]
            record.taxable_income = row[4]
            record.tax_amount = row[5]
            record.tax_type = row[6]
            record.description = row[7]
            record.created_at = row[8]
            tax_records.append(record)
        
        return tax_records
    
    @classmethod
    def get_by_employee(cls, employee_id: int):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, employee_id, period, gross_income, taxable_income, tax_amount, tax_type, description, created_at FROM tax_records WHERE employee_id=? ORDER BY period DESC', (employee_id,))
        rows = cursor.fetchall()
        conn.close()
        
        tax_records = []
        for row in rows:
            record = cls()
            record.id = row[0]
            record.employee_id = row[1]
            record.period = row[2]
            record.gross_income = row[3]
            record.taxable_income = row[4]
            record.tax_amount = row[5]
            record.tax_type = row[6]
            record.description = row[7]
            record.created_at = row[8]
            tax_records.append(record)
        
        return tax_records
    
    @classmethod
    def get_by_period(cls, period: str):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, employee_id, period, gross_income, taxable_income, tax_amount, tax_type, description, created_at FROM tax_records WHERE period=?', (period,))
        rows = cursor.fetchall()
        conn.close()
        
        tax_records = []
        for row in rows:
            record = cls()
            record.id = row[0]
            record.employee_id = row[1]
            record.period = row[2]
            record.gross_income = row[3]
            record.taxable_income = row[4]
            record.tax_amount = row[5]
            record.tax_type = row[6]
            record.description = row[7]
            record.created_at = row[8]
            tax_records.append(record)
        
        return tax_records