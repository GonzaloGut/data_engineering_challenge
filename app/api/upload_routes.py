import io
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.department import Department

router = APIRouter()

@router.post("/upload/departments")
async def upload_departments(
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
        "department"
    ]

    departments = []

    for _, row in df.iterrows():
        
        department = Department(
            id=row["id"],
            department=row["department"]
        )   
        
        departments.append(department)
    
    db.bulk_save_objects(departments)

    db.commit()

    return {
        "message": "Departments uploaded successfully",
        "rows_inserted": len(departments)
    }
