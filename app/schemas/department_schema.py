from pydantic import BaseModel

class DepartmentSchema(BaseModel):
    id: int
    department: str