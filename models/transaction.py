from dataclasses import dataclass
from typing import Optional
import sqlite3
from config.database import db_manager

@dataclass
class Transaction:
    id: Optional[int] = None
    type: str = "penjualan"  # penjualan/belanja
    description: str = ""
    amount: float = 0.0
    ppn_amount: float = 0.0
    transaction_date: str = ""
    invoice_number: Optional[str] = None
    
    def save(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO transactions 
                (type, description, amount, ppn_amount, transaction_date, invoice_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.type, self.description, self.amount, self.ppn_amount,
                  self.transaction_date, self.invoice_number))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE transactions 
                SET type=?, description=?, amount=?, ppn_amount=?, transaction_date=?, invoice_number=?
                WHERE id=?
            ''', (self.type, self.description, self.amount, self.ppn_amount,
                  self.transaction_date, self.invoice_number, self.id))
        
        conn.commit()
        conn.close()
    
    @classmethod
    def get_all(cls):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions ORDER BY transaction_date DESC, id DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
    
    @classmethod
    def get_by_id(cls, trans_id):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE id=?', (trans_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
    
    def delete(self):
        if self.id:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions WHERE id=?', (self.id,))
            conn.commit()
            conn.close()