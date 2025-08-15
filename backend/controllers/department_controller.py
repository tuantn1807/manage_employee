from models.department import Department
from config.db import engine
from bson import ObjectId
from fastapi import HTTPException
from typing import List

async def create_department(departments: List[Department]) -> List[Department]:
    await engine.save_all(departments)
    return departments

async def get_all_departments() -> List[Department]:
    return await engine.find(Department)

async def get_department_by_id(dept_id: str) -> Department:
    dept = await engine.find_one(Department, Department.id == ObjectId(dept_id))
    if not dept:
        raise HTTPException(status_code=404, detail="Phòng không tồn tại")
    return dept

async def update_department(dept_id: str, data: Department) -> Department:
    dept = await get_department_by_id(dept_id)
    dept.name = data.name
    dept.chief_id = data.chief_id
    await engine.save(dept)
    return dept

async def delete_department(dept_id: str):
    dept = await get_department_by_id(dept_id)
    await engine.delete(dept)
