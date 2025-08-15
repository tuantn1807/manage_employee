from fastapi import HTTPException
from models.request_form import RequestForm, RequestStatus
from models.attendance import Attendance
from models.employee import Employee
from models.department import Department
from config.db import engine
from datetime import datetime, time
from bson import ObjectId


async def submit_request_logic(form: RequestForm, current_user: Employee):
    form.employee_id = current_user.id
    form.created_at = datetime.now()
    form.updated_at = datetime.now()
    # Chuyển datetime -> date nếu cần
    form.date = datetime.combine(form.date, time.min)
    await engine.save(form)
    return {"message": "Đã gửi đơn thành công"}

async def approve_request_logic(request_id: str, current_user: Employee):
    request = await engine.find_one(RequestForm, RequestForm.id == ObjectId(request_id))
    if not request:
        raise HTTPException(404, "Không tìm thấy đơn")

    department = await engine.find_one(Department, Department.id == current_user.department_id)
    if department.chief_id != current_user.id:
        raise HTTPException(403, "Bạn không có quyền duyệt")

    request.status = RequestStatus.approved
    request.updated_at = datetime.now()
    await engine.save(request)

    day_start = datetime.combine(request.date.date(), time(0, 0))
    day_end = datetime.combine(request.date.date(), time(23, 59, 59))
    old_att = await engine.find(
        Attendance,
        (Attendance.employee_id == request.employee_id) &
        (Attendance.date >= day_start) &
        (Attendance.date <= day_end)
    )
    
    for att in old_att:
        await engine.delete(att)

    sessions = []
    if request.session in ["sang", "ca ngay"]:
        sessions.append(time(8, 0))
    if request.session in ["chieu", "ca ngay"]:
        sessions.append(time(13, 0))
    employee = await engine.find_one(Employee, Employee.id == request.employee_id)
    if not employee:
        raise HTTPException(404, "Không tìm thấy nhân viên")

    for t in sessions:
        att = Attendance(
            employee_id=request.employee_id,
            department_id=employee.department_id,  # Thêm department_id
            date=datetime.combine(request.date.date(), t),
            status="absent_per"
    )
        await engine.save(att)

    return {"message": "Đã duyệt đơn và cập nhật điểm danh"}


async def reject_request_logic(request_id: str, current_user: Employee):
    request = await engine.find_one(RequestForm, RequestForm.id == ObjectId(request_id))
    if not request:
        raise HTTPException(404, "Không tìm thấy đơn")

    department = await engine.find_one(Department, Department.id == current_user.department_id)
    if department.chief_id != current_user.id:
        raise HTTPException(403, "Bạn không có quyền từ chối")

    request.status = RequestStatus.rejected
    request.updated_at = datetime.now()
    await engine.save(request)
    return {"message": "Đã từ chối đơn"}


async def get_my_requests_logic(current_user: Employee):
    return await engine.find(RequestForm, RequestForm.employee_id == current_user.id)


async def get_department_requests_logic(current_user: Employee):
    department = await engine.find_one(Department, Department.id == current_user.department_id)
    if not department or department.chief_id != current_user.id:
        raise HTTPException(403, "Bạn không có quyền xem")

    employees = await engine.find(Employee, Employee.department_id == department.id)
    employee_ids = [e.id for e in employees]
    return await engine.find(RequestForm, {"employee_id": {"$in": employee_ids}})

