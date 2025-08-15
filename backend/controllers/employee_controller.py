from models.employee import Employee
from bson import ObjectId
from odmantic import AIOEngine
from fastapi import HTTPException
from typing import List
from config.db import engine
from datetime import datetime
from utils.auth_utils import hash_password
from models.department import Department
async def create_employee(employee_data: Employee):
    data = employee_data.dict()  
    if not data.get("join_date"):
        data["join_date"] = datetime.now()

    raw_pwd = data.get("pwd") or "a"
    data["pwd"] = hash_password(raw_pwd)

    employee = Employee(**data)
    await engine.save(employee)
    return employee

async def get_all_employees() -> List[Employee]:
    return await engine.find(Employee)

async def get_all_employees_with_department_name() -> List[dict]:
    employees = await engine.find(Employee)
    result = []
    for emp in employees:
        dept_name = None
        if emp.department_id:
            department = await engine.find_one(Department, Department.id == emp.department_id)
            if department:
                dept_name = department.name
        result.append({
            "id": str(emp.id),
            "full_name": emp.full_name,
            "uname": emp.uname,
             "pwd": emp.pwd,
            "email": emp.email,
            "phone": emp.phone,
            "birthday": emp.birthday,
            "gender": emp.gender,
            "join_date": emp.join_date,
            "position": emp.position,
            "department_id": str(emp.department_id) if emp.department_id else None,
            "department_name": dept_name
        })
    return result

async def get_employee_by_id(emp_id: str) -> Employee:
    emp = await engine.find_one(Employee, Employee.id == ObjectId(emp_id))
    if not emp:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhân viên")
    return emp

async def update_employee(emp_id: str, data: dict) -> Employee:
    emp = await get_employee_by_id(emp_id)
    if not emp:
        raise ValueError("Không tìm thấy nhân viên")

    for field, value in data.items():
        if field != "id" and hasattr(emp, field):
            setattr(emp, field, value)

    await engine.save(emp)
    return emp


async def delete_employee(emp_id: str):
    emp = await get_employee_by_id(emp_id)
    await engine.delete(emp)

