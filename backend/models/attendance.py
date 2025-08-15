from odmantic import Model
from bson import ObjectId
from datetime import datetime
class Attendance(Model):
    employee_id: ObjectId
    department_id: ObjectId
    date: datetime
    status: str 
