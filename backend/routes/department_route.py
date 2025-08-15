from fastapi import APIRouter
from models.department import Department
from controllers import department_controller as ctrl
from typing import List

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=List[Department])
async def create(dept: List[Department]):
    return await ctrl.create_department(dept)

@router.get("/", response_model=List[Department])
async def read_all():
    return await ctrl.get_all_departments()

@router.get("/{dept_id}", response_model=Department)
async def read_one(dept_id: str):
    return await ctrl.get_department_by_id(dept_id)

@router.put("/{dept_id}", response_model=Department)
async def update(dept_id: str, data: Department):
    return await ctrl.update_department(dept_id, data)

@router.delete("/{dept_id}")
async def delete(dept_id: str):
    await ctrl.delete_department(dept_id)
    return {"message": "Xoá thành công"}
