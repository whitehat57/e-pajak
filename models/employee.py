from dataclasses import dataclass
from typing import Optional
import sqlite3
from config.database import db_manager

@dataclass
class Employee:
    id: Optional[int] = None
    name: str = ""
    status: str = "tetap"  # tetap/tidak_tetap
    monthly_salary: float = 0.0
    allowances: float = 0.0
    npwp: Optional[str] = None
    
    def save(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO employees (name, status, monthly_salary, allowances, npwp)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.name, self.status, self.monthly_salary, self.allowances, self.npwp))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE employees 
                SET name=?, status=?, monthly_salary=?, allowances=?, npwp=?
                WHERE id=?
            ''', (self.name, self.status, self.monthly_salary, self.allowances, self.npwp, self.id))
        
        conn.commit()
        conn.close()
    
    @classmethod
    def get_all(cls):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_by_id(cls, emp_id):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id=?', (emp_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    def delete(self):
        if self.id:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM employees WHERE id=?', (self.id,))
            conn.commit()
            conn.close()