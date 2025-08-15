from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine
from typing import List, Optional
from models.salary import Salary, SalaryInput
from config.db import get_engine
from controllers import salary_controller as ctrl
from models.employee import Employee
from controllers.salary_controller import get_current_employee 
router = APIRouter(prefix="/api/salary", tags=["Salary"])
@router.post("/calculate", response_model=List[Salary])
async def calculate_all_salary_route(
    month: int,
    year: int,
    engine: AIOEngine = Depends(get_engine)
):
    salaries = await ctrl.calculate_salaries(engine, month, year)
    return salaries
@router.get("/employee/{employee_id}", response_model=List[Salary])
async def get_salaries_of_employee(
    employee_id: str,
    month: Optional[int] = None,
    year: Optional[int] = None,
    engine: AIOEngine = Depends(get_engine)
):
    return await ctrl.get_salaries_by_employee(engine, employee_id, month, year)

# Bổ sung API cho nhân viên tự xem lương của mình
@router.get("/mine", response_model=List[Salary])
async def get_my_salaries(
    employee_id: str,  
    month: Optional[int] = None,
    year: Optional[int] = None,
    engine: AIOEngine = Depends(get_engine)
):
    return await ctrl.get_salaries_by_employee(engine, employee_id, month, year)

@router.get("/", response_model=List[Salary])
async def get_all(engine: AIOEngine = Depends(get_engine)):
    return await ctrl.get_all_salaries(engine)