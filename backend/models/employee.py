from odmantic import Model
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Employee(Model):
    full_name: str
    uname: str
    pwd: str
    email: Optional[str]=None
    phone: Optional[str]=None
    birthday: Optional[datetime]=None
    gender: Optional[str]=None
    department_id: Optional[ObjectId]=None  
    join_date: Optional[datetime]=None
    position:Optional[str] = None
