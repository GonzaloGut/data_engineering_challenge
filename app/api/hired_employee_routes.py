import io
from datetime import datetime, UTC
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.dependencies import get_db
from app.models.hired_employee import HiredEmployee
from app.utils.file_validation import validate_csv_file

router = APIRouter()

@router.post("/upload/employees")
async def upload_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    # Validate uploaded file
    await validate_csv_file(file)
    
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    
    # Bronze Layer: Save raw CSV
    bronze_path = (
        f"storage/bronze/employees_{timestamp}.csv"
    )

    contents = await file.read()

    with open(bronze_path, "wb") as bronze_file:
        bronze_file.write(contents)

    # Read CSV
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

    # Clean numeric columns

    df["id"] = pd.to_numeric(
        df["id"],
        errors="coerce"
    ).astype("Int64")

    df["department_id"] = pd.to_numeric(
        df["department_id"],
        errors="coerce"
    ).astype("Int64")

    df["job_id"] = pd.to_numeric(
        df["job_id"],
        errors="coerce"
    ).astype("Int64")

    
    # Validate datetime
    
    df["datetime"] = pd.to_datetime(
        df["datetime"],
        errors="coerce"
    )
    
    # Split valid/invalid rows
    
    invalid_rows = df[
        (df["datetime"].isnull()) | 
        (df["id"].isnull()) |
        (df["department_id"].isnull()) |
        (df["job_id"].isnull())
    ]

    valid_rows = df.drop(invalid_rows.index)

    # Save INVALID rows
    invalid_rows_count = len(invalid_rows)
    if invalid_rows_count > 0:
        error_path = (
            f"storage/errors/hired_employees_invalid_{timestamp}.csv"
        )
        invalid_rows.to_csv(error_path, index=False)
    
    # Save VALID rows (INSERT)
    
    employees = []

    for _, row in valid_rows.iterrows():
        
        employee = HiredEmployee(
            id=int(row["id"]),
            name=row["name"],
            datetime=row["datetime"],
            department_id=int(row["department_id"]),
            job_id=int(row["job_id"])
        )   
        
        employees.append(employee)
    
    try:
        db.bulk_save_objects(employees)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Foreign key violation or duplicate ID"
        )
    
    return {
        "message": "Employees uploaded successfully",
        "rows_inserted": len(employees),
        "invalid_rows": invalid_rows_count
    }
