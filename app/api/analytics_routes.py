from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.dependencies import get_db

router = APIRouter()

@router.get("/analytics/employees_by_quarter")
# Number of employees hired for each job and department in 2021 divided by quarter, 
#   ordered alphabetically by department and job.

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


@router.get("/analytics/departments_above_mean")
# List of ids, name and number of employees hired of each department that hired more
#  employees than the mean of employees hired in 2021 for all the departments,
#  ordered by the number of employees hired (descending)

def departments_above_mean(
    db: Session = Depends(get_db)
):
    query = text("""
                 WITH department_hires AS (
                    SELECT d.id,
                        d.department,
                        COUNT(he.id) AS hired
                    
                    FROM hired_employees he
                    INNER JOIN departments d ON he.department_id = d.id
                    WHERE EXTRACT(YEAR FROM he.datetime) = 2021
                    GROUP BY d.id, d.department
                 )

                 
                 SELECT id,
                    department,
                    hired
                             
                 FROM department_hires
                 WHERE hired > (
                        SELECT AVG(hired)
                        FROM department_hires
                    )
                 ORDER BY hired DESC
                 
                 """)   
    
    result = db.execute(query)
    rows = result.mappings().all()
    return rows