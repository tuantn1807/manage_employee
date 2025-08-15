from fastapi import APIRouter, Depends, HTTPException, Header
from models.employee import Employee
from models.department import Department
from models.attendance import Attendance
from config.db import engine
from bson import ObjectId
from datetime import date
from datetime import datetime,time,timedelta
from typing import List, Optional
from fastapi import Query
from typing import Optional
from models.request_form import RequestForm,RequestStatus
from typing import Literal
router = APIRouter()

# Định nghĩa hàm này trước các endpoint
async def get_current_employee(x_user_id: str = Header(...)):
    user = await engine.find_one(Employee, Employee.id == ObjectId(x_user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhân viên")
    return user

@router.get("/employees/department")
async def get_employees_of_department(current_user: Employee = Depends(get_current_employee)):
    department = await engine.find_one(Department, Department.chief_id == current_user.id)
    if not department:
        raise HTTPException(status_code=403, detail="Bạn không phải trưởng phòng")
    employees = await engine.find(Employee, Employee.department_id == department.id)
    return [
        {
            "id": str(emp.id),
            "full_name": getattr(emp, "full_name", ""),
            "name": getattr(emp, "name", "")
        }
        for emp in employees
    ]

@router.post("/attendance/mark")
async def mark_attendance(attendance: List[dict], current_user: Employee = Depends(get_current_employee)):
    department = await engine.find_one(Department, Department.chief_id == current_user.id)
    if not department:
        raise HTTPException(status_code=403, detail="Bạn không phải trưởng phòng")

    for item in attendance:
        emp_id = item.get("emp_id")
        status = item.get("status")

        if not emp_id or not status:
            continue

    
        now = datetime.now()

     
        start_of_day = datetime.combine(now.date(), time.min)
        end_of_day = datetime.combine(now.date(), time.max)

        approved_request = await engine.find_one(
            RequestForm,
            (RequestForm.employee_id == ObjectId(emp_id)) &
            (RequestForm.date >= start_of_day) &
            (RequestForm.date <= end_of_day) &
            (RequestForm.status == RequestStatus.approved)
        )

        reason = approved_request.reason if approved_request else None

        employee = await engine.find_one(Employee, Employee.id == ObjectId(emp_id))
        if not employee:
            continue

        att = Attendance(
            employee_id=employee.id,
            department_id=department.id,
            date=now,  
            status=status,
            reason=reason
        )
        await engine.save(att)

    return {"msg": "Lưu điểm danh thành công (dùng thời gian thực của backend)"}
@router.get("/attendance/mine")
async def get_my_attendance_issues(
    current_user: Employee = Depends(get_current_employee),
    status: Optional[str] = Query(None, description="Lọc theo trạng thái"),
    buoi: Optional[str] = Query(None, description="Lọc theo buổi (sang/chieu)")
):
    absences = await engine.find(
        Attendance,
        Attendance.employee_id == current_user.id
    )

    result = []
    for a in absences:
        # Lọc theo trạng thái
        if status and a.status != status:
            continue

        # Tính buổi dựa trên giờ
        buoi_val = None
        try:
            hour = a.date.hour
            buoi_val = "sang" if hour < 12 else "chieu"
        except:
            buoi_val = None

        if buoi and buoi != buoi_val:
            continue

        result.append({
            "id": str(a.id),
            "date": a.date.isoformat() if a.date else None,
            "status": a.status,
            "reason": getattr(a, "reason", None),
            "buoi": buoi_val
        })

    return result

from datetime import datetime


@router.get("/request/approved")
async def get_approved_requests(
    date: datetime = Query(..., description="Ngày cần lấy đơn"),
    session: str = Query(..., pattern="^(sang|chieu)$", description="Buổi (sang hoặc chieu)"),
):
    # Đặt khoảng thời gian từ đầu ngày đến cuối ngày
    date_start = datetime(date.year, date.month, date.day, 0, 0, 0)
    date_end = date_start + timedelta(days=1)

    requests = await engine.find(
        RequestForm,
        (RequestForm.status == "approved") &
        (RequestForm.date >= date_start) & (RequestForm.date < date_end) &  # 👈 so sánh theo khoảng ngày
        (RequestForm.session == session) &
        ((RequestForm.type == "absent_per") | (RequestForm.type == "late"))
    )

    # Log để kiểm tra
    print(f" Approved requests on {date.date()} ({session}): {len(requests)} đơn")
    for r in requests:
        print(f"{r.employee_id} - {r.type} - {r.date}")

    return [
        {
            "employee_id": str(req.employee_id),
            "type": req.type
        }
        for req in requests
    ]