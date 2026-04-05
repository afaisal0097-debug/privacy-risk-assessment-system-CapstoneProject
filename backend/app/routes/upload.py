from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path

from app.services.validate import (
    save_upload_file,
    extract_columns,
    validate_quasi_and_sensitive_attributes,
)

router = APIRouter()

REAL_STORAGE_DIR = Path("storage/real")
SYNTHETIC_STORAGE_DIR = Path("storage/synthetic")

REAL_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
SYNTHETIC_STORAGE_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_datasets(
    real_file: UploadFile = File(...),
    synthetic_file: UploadFile = File(...),
    quasi_identifiers: list[str] = Form(...),
    sensitive_attributes: list[str] = Form(...)
):
    if not real_file:
        raise HTTPException(status_code=400, detail="Real dataset file is required")

    if not synthetic_file:
        raise HTTPException(status_code=400, detail="Synthetic dataset file is required")

    if not quasi_identifiers:
        raise HTTPException(status_code=400, detail="At least one quasi identifier is required")

    if not sensitive_attributes:
        raise HTTPException(status_code=400, detail="At least one sensitive attribute is required")

    real_path = None
    synthetic_path = None

    try:
        real_stored_filename, real_path, real_size, real_ext = await save_upload_file(
            upload_file=real_file,
            storage_dir=REAL_STORAGE_DIR
        )

        synthetic_stored_filename, synthetic_path, synthetic_size, synthetic_ext = await save_upload_file(
            upload_file=synthetic_file,
            storage_dir=SYNTHETIC_STORAGE_DIR
        )

        real_columns = extract_columns(real_path)
        synthetic_columns = extract_columns(synthetic_path)

        validated_fields = validate_quasi_and_sensitive_attributes(
            quasi_identifiers=quasi_identifiers,
            sensitive_attributes=sensitive_attributes,
            real_columns=real_columns,
            synthetic_columns=synthetic_columns
        )

        common_columns = sorted(list(set(real_columns).intersection(set(synthetic_columns))))
        real_only_columns = sorted(list(set(real_columns) - set(synthetic_columns)))
        synthetic_only_columns = sorted(list(set(synthetic_columns) - set(real_columns)))

        return {
            "message": "Datasets uploaded successfully",
            "status": "validated",
            "quasi_identifiers": validated_fields["quasi_identifiers"],
            "sensitive_attributes": validated_fields["sensitive_attributes"],
            "real_file": {
                "original_filename": real_file.filename,
                "stored_filename": real_stored_filename,
                "path": str(real_path),
                "size_bytes": real_size,
                "extension": real_ext,
                "columns": real_columns,
            },
            "synthetic_file": {
                "original_filename": synthetic_file.filename,
                "stored_filename": synthetic_stored_filename,
                "path": str(synthetic_path),
                "size_bytes": synthetic_size,
                "extension": synthetic_ext,
                "columns": synthetic_columns,
            },
            "common_columns": common_columns,
            "real_only_columns": real_only_columns,
            "synthetic_only_columns": synthetic_only_columns,
        }

    except HTTPException:
        if real_path and real_path.exists():
            real_path.unlink()
        if synthetic_path and synthetic_path.exists():
            synthetic_path.unlink()
        raise

    except Exception as e:
        if real_path and real_path.exists():
            real_path.unlink()
        if synthetic_path and synthetic_path.exists():
            synthetic_path.unlink()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")