from odmantic import Model
from typing import Optional
from bson import ObjectId

class Department(Model):
    name: str
    chief_id: Optional[ObjectId] = None
