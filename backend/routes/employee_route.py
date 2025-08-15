from fastapi import APIRouter
from models.employee import Employee
from controllers import employee_controller as ctrl
from typing import List
from fastapi import Body
from typing import Optional
router = APIRouter(prefix="/employees", tags=["Employees"])
class EmployeeWithDepartment(Employee):
    department_name: Optional[str] = None

@router.post("/", response_model=Employee)
async def create(emp: Employee):
    return await ctrl.create_employee(emp)

@router.get("/", response_model=List[Employee])
async def get_all():
    return await ctrl.get_all_employees()

@router.get("/with_department", response_model=List[EmployeeWithDepartment])
async def get_all():
    return await ctrl.get_all_employees_with_department_name()

@router.get("/{emp_id}", response_model=Employee)
async def get_by_id(emp_id: str):
    return await ctrl.get_employee_by_id(emp_id)

@router.put("/{emp_id}", response_model=Employee)
async def update(emp_id: str, data: dict = Body(...)):
    return await ctrl.update_employee(emp_id, data)
@router.delete("/{emp_id}")
async def delete(emp_id: str):
    await ctrl.delete_employee(emp_id)
    return {"message": "Đã xoá nhân viên"}
