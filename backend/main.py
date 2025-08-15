from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.department_route import router  as department_router
from routes.employee_route import router as employee_router
from routes.auth_route import router as auth_router
from routes.attendance_route import router as attendance_router
from routes.salary_route import router as salary_router
from routes.request_route import router as request_router
app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(attendance_router, prefix="/api")
app.include_router(salary_router)
app.include_router(request_router, prefix="/api")
