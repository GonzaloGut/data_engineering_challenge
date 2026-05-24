from fastapi import FastAPI
from app.database.database import Base, engine
from app.models.department import Department
from app.models.job import Job
from app.models.hired_employee import HiredEmployee
from app.api.upload_routes import router as upload_router

app = FastAPI(
    title="Data Engineering Challenge API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(upload_router)

@app.get("/")
def healtcheck():
    return {"status": "ok", "service": "Data Engineering Challenge API"}
