from fastapi import HTTPException, UploadFile

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_CONTENT_TYPES = {
    "text/csv",
    "application/vnd.ms-excel",
}


async def validate_csv_file(file: UploadFile) -> None:
    """
    Validates the uploaded CSV file.

    Checks:
    - .csv extension
    - Allowed MIME type
    - Maximum file size
    """

    # Validate file extension
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="File must be a CSV."
        )

    # Validate MIME type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only CSV files are allowed."
        )

    contents = await file.read()

    # Validate file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the maximum allowed size (10 MB)."
        )

    # Reset file pointer for later use
    await file.seek(0)