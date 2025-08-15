
from odmantic import Model, ObjectId
from typing import Optional
from datetime import datetime

class Salary(Model):
    employee_id: ObjectId
    month: int
    year: int
    basic_salary: float  
    work_days: float      
    allowance: float     
    bhxh_employee: float 
    bhxh_company: float  
    total_salary: float 
    net_salary: float    
    created_at: datetime = datetime.now()
class SalaryInput(Model):
    month: int
    year: int
