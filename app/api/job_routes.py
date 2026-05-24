import io
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.job import Job

router = APIRouter()

@router.post("/upload/jobs")
async def upload_jobs(
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
        "job"
    ]

    jobs = []

    for _, row in df.iterrows():
        
        job = Job(
            id=row["id"],
            job=row["job"]
        )   
        
        jobs.append(job)
    
    db.bulk_save_objects(jobs)

    db.commit()

    return {
        "message": "Jobs uploaded successfully",
        "rows_inserted": len(jobs)
    }
