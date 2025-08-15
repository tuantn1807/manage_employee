# controllers/salary_controller.py
from models.salary import Salary
from models.employee import Employee
from models.attendance import Attendance
from odmantic import AIOEngine
from datetime import datetime,time
from bson import ObjectId
from models.department import Department
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from config.db import engine
BHXH_EMPLOYEE_RATE = 0.105
BHXH_COMPANY_RATE = 0.215
BHXH_EMPLOYEE_RATE = 0.105
BHXH_COMPANY_RATE = 0.215
DEFAULT_SALARY = 4_000_000
POSITION_SALARY = {
    "ceo": 9_000_000,
    "engineer": 6_000_000,
    "accountant": 4_500_000,
    "architect": 7_000_000,
    "project sales staff": 4_200_000,
    "market development staff": 4_200_000,
}

async def get_current_employee(x_user_id: str = Header(...)):
    user = await engine.find_one(Employee, Employee.id == ObjectId(x_user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhân viên")
    return user

async def calculate_salaries(engine: AIOEngine, month: int, year: int):
    employees = await engine.find(Employee)
    departments = await engine.find(Department)
    dept_dict = {dept.id: dept for dept in departments}

    salaries = []
    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    for employee in employees:
        # Check if employee is CEO
        position = employee.position.lower()
        if position == "ceo":
            work_days = 26  # CEO always gets full work days
        else:
            # Get valid attendance records
            attendances = await engine.find(
                Attendance,
                (Attendance.employee_id == employee.id) &
                (Attendance.date >= start_date) &
                (Attendance.date < end_date) &
                ((Attendance.status == "present") | (Attendance.status == "absent_per"))
            )

            # Group by morning/afternoon sessions
            day_sessions = {}
            for att in attendances:
                day = att.date.date()
                session_key = "sang" if att.date.hour < 12 else "chieu"
                if day not in day_sessions:
                    day_sessions[day] = {}
                day_sessions[day][session_key] = att.date

            # Calculate work days
            work_days = 0
            for day, sessions in day_sessions.items():
                is_sunday = day.weekday() == 6
                for _, dt in sessions.items():
                    is_overtime = is_sunday or dt.time() > time(17, 30)
                    work_days += 1 if is_overtime else 0.5

        # Calculate basic salary based on position
        basic_salary = POSITION_SALARY.get(position, 8_000_000)

        # Check if department chief
        department = dept_dict.get(employee.department_id)
        if department and department.chief_id == employee.id:
            basic_salary *= 1.5

        # Calculate final salary
        total_salary = basic_salary * work_days / 26
        bhxh_employee = total_salary * BHXH_EMPLOYEE_RATE
        bhxh_company = total_salary * BHXH_COMPANY_RATE
        allowance = 1_500_000
        net_salary = total_salary + allowance - bhxh_employee

        salary = Salary(
            employee_id=employee.id,
            month=month,
            year=year,
            basic_salary=basic_salary,
            work_days=work_days,
            allowance=allowance,
            bhxh_employee=bhxh_employee,
            bhxh_company=bhxh_company,
            total_salary=total_salary,
            net_salary=net_salary,
            created_at=datetime.now()
        )

        await engine.save(salary)
        salaries.append(salary)

    return salaries





async def get_salary_by_employee_and_month(engine: AIOEngine, employee: Employee) -> float:
    if not employee or not employee.department_id:
        return DEFAULT_SALARY
    

    position = getattr(employee, "position", "").lower()
    
    base_salary = DEFAULT_SALARY
    for key in POSITION_SALARY:
        if key in position:
            base_salary = POSITION_SALARY[key]
            break

    department = await engine.find_one(Department, Department.id == employee.department_id)
    if department and department.chief_id == employee.id:
        base_salary *= 1.5

    return base_salary
async def get_salaries_by_employee(engine: AIOEngine, employee_id: str, month: Optional[int] = None, year: Optional[int] = None) -> List[Salary]:
    query = {"employee_id": ObjectId(employee_id)}
    if month:
        query["month"] = month
    if year:
        query["year"] = year

    return await engine.find(Salary, query)
async def get_all_salaries(engine: AIOEngine):

    return await engine.find(Salary)
