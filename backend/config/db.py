from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
engine = AIOEngine(client=client, database="my_db")
def get_engine() -> AIOEngine:
    return engine