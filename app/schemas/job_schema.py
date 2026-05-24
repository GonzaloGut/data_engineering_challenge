from pydantic import BaseModel

class JobSchema(BaseModel):
    id: int
    job: str