from fastapi import APIRouter, HTTPException
from models.employee import Employee
from schemas.auth_schema import LoginByUsername
from config.db import engine
from utils.auth_utils import verify_password
from models.department import Department
from bson import ObjectId
router = APIRouter()

# @router.post("/login")
# async def login(data: LoginByUsername):
#     user = await engine.find_one(Employee, Employee.uname == data.uname)
#     if not user or not verify_password(data.pwd, user.pwd):
#         raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng")
#     return {"message": "Đăng nhập thành công", "full_name": user.full_name}
@router.post("/login")
async def login(data: LoginByUsername):
    user = await engine.find_one(Employee, Employee.uname == data.uname)
    if not user or not verify_password(data.pwd, user.pwd):
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng")
    
    # Kiểm tra có phải trưởng phòng không
    department = await engine.find_one(Department, Department.chief_id == user.id)
    is_chief = department is not None
    
    return {
        "message": "Đăng nhập thành công",
        "full_name": user.full_name,
        "department_id": str(user.department_id),
        "id": str(user.id),
        "position": user.position,  
        "is_chief": is_chief
    }
