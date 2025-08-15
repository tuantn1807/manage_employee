from fastapi import APIRouter, Depends, HTTPException
from models.request_form import RequestForm, RequestStatus
from models.employee import Employee
from controllers import request_controller
from controllers.salary_controller import get_current_employee
from datetime import datetime,time

from config.db import engine  # Nếu `engine.find()` được sử dụng, bạn cần import engine đúng cách

router = APIRouter()

@router.post("/request")
async def submit_request(
    form: RequestForm, 
    current_user: Employee = Depends(get_current_employee)
):
    return await request_controller.submit_request_logic(form, current_user)


@router.put("/request/{request_id}/approve")
async def approve_request(
    request_id: str, 
    current_user: Employee = Depends(get_current_employee)
):
    return await request_controller.approve_request_logic(request_id, current_user)


@router.put("/request/{request_id}/reject")
async def reject_request(
    request_id: str, 
    current_user: Employee = Depends(get_current_employee)
):
    return await request_controller.reject_request_logic(request_id, current_user)


@router.get("/request/mine")
async def get_my_requests(
    current_user: Employee = Depends(get_current_employee)
):
    return await request_controller.get_my_requests_logic(current_user)


@router.get("/request/department")
async def get_department_requests(
    current_user: Employee = Depends(get_current_employee)
):
    return await request_controller.get_department_requests_logic(current_user)


