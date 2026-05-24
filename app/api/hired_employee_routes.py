import io
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.hired_employee import HiredEmployee

router = APIRouter()

@router.post("/upload/employees")
async def upload_employees(
    file: UploadFile = File(...),
    db : Session = Depends(get_db)
):
    
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="File must be a CSV"
        )
    
    contents = await file.read()

    df = pd.read_csv(
        io.StringIO(contents.decode("utf-8")),
        header=None
    )

    df.columns = [
        "id",
        "name",
        "datetime",
        "department_id",
        "job_id"
    ]

    try: 
        df["datetime"] = pd.to_datetime(df["datetime"])
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime format"
        )

    employees = []

    for _, row in df.iterrows():
        
        employee = HiredEmployee(
            id=row["id"],
            name=row["name"],
            datetime=row["datetime"],
            department_id=row["department_id"],
            job_id=row["job_id"]
        )   
        
        employees.append(employee)
    
    db.bulk_save_objects(employees)

    db.commit()

    return {
        "message": "Employees uploaded successfully",
        "rows_inserted": len(employees)
    }
