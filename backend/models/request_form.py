from odmantic import Model
from datetime import date,datetime
from enum import Enum
from bson import ObjectId

class RequestType(str, Enum):
    absent_per = "absent_per"
    late = "late"

class RequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class RequestForm(Model):
    employee_id: ObjectId
    type: RequestType
    reason: str
    date: datetime
    session: str  # "sang", "chieu", "ca ngay"
    status: RequestStatus = RequestStatus.pending
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()