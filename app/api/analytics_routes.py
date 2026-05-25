from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.dependencies import get_db

router = APIRouter()

@router.get("/analytics/employees_by_quarter")
# Number of employees hired for each job and department in 2021 divided by quarter.

def employees_by_quarter(
    db: Session = Depends(get_db)
):
    query = text("""
                 SELECT d.department, 
                    j.job,
                    
                    SUM(
                        CASE
                            WHEN EXTRACT(QUARTER FROM he.datetime) = 1 THEN 1
                            ELSE 0
                        END
                    ) AS Q1,
                 
                    SUM(
                        CASE
                            WHEN EXTRACT(QUARTER FROM he.datetime) = 2 THEN 1
                            ELSE 0
                        END
                    ) AS Q2,
                 
                    SUM(
                        CASE
                            WHEN EXTRACT(QUARTER FROM he.datetime) = 3 THEN 1
                            ELSE 0
                        END
                    ) AS Q3,
                 
                    SUM(
                        CASE
                            WHEN EXTRACT(QUARTER FROM he.datetime) = 4 THEN 1
                            ELSE 0
                        END
                    ) AS Q4

                 FROM hired_employees he
                 INNER JOIN departments d ON he.department_id = d.id
                 INNER JOIN jobs j ON he.job_id = j.id

                 WHERE EXTRACT(YEAR FROM he.datetime) = 2021
                 GROUP BY d.department, j.job
                 ORDER BY d.department, j.job

                 """)   
    
    result = db.execute(query)
    rows = result.mappings().all()
    return rows