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
    created_at: Optional[str] = None
    
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
        cursor.execute('SELECT id, name, status, monthly_salary, allowances, npwp, created_at FROM employees')
        rows = cursor.fetchall()
        conn.close()
        
        employees = []
        for row in rows:
            employee = cls()
            employee.id = row[0]
            employee.name = row[1]
            employee.status = row[2]
            employee.monthly_salary = row[3]
            employee.allowances = row[4]
            employee.npwp = row[5]
            employee.created_at = row[6]
            employees.append(employee)
        
        return employees
    
    @classmethod
    def get_by_id(cls, emp_id):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, status, monthly_salary, allowances, npwp, created_at FROM employees WHERE id=?', (emp_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            employee = cls()
            employee.id = row[0]
            employee.name = row[1]
            employee.status = row[2]
            employee.monthly_salary = row[3]
            employee.allowances = row[4]
            employee.npwp = row[5]
            employee.created_at = row[6]
            return employee
        return None
    
    def delete(self):
        if self.id:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM employees WHERE id=?', (self.id,))
            conn.commit()
            conn.close()