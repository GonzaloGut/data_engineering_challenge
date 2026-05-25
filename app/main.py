from fastapi import FastAPI
from app.database.database import Base, engine
from app.models.department import Department
from app.models.job import Job
from app.models.hired_employee import HiredEmployee
from app.api.department_routes import router as department_router
from app.api.job_routes import router as job_router
from app.api.hired_employee_routes import router as employee_router
from app.api.analytics_routes import router as analytics_router

app = FastAPI(
    title="Data Engineering Challenge API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(department_router)
app.include_router(job_router)
app.include_router(employee_router)
app.include_router(analytics_router)

@app.get("/")
def healtcheck():
    return {"status": "ok", "service": "Data Engineering Challenge API"}
