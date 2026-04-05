from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

from app.services.validate import (
    save_upload_file,
    extract_columns,
    validate_quasi_and_sensitive_attributes,
)
from app.database import get_db
from app.repositories import insert_dataset_upload, bulk_insert_real_records, bulk_insert_synthetic_records
from app.models import DatasetKind

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
    sensitive_attributes: list[str] = Form(...),
    db: Session = Depends(get_db)
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

        # Read dataframes
        if real_ext == ".csv":
            real_df = pd.read_csv(real_path)
        else:
            real_df = pd.read_excel(real_path)

        if synthetic_ext == ".csv":
            synthetic_df = pd.read_csv(synthetic_path)
        else:
            synthetic_df = pd.read_excel(synthetic_path)

        # Insert metadata for real file
        real_file_uuid = insert_dataset_upload(
            db=db,
            dataset_kind=DatasetKind.real,
            input_filename=real_file.filename,
            stored_filename=real_stored_filename,
            file_path=str(real_path),
            file_extension=real_ext,
            file_size_bytes=real_size,
            mime_type=real_file.content_type,
            row_count=len(real_df),
            column_count=len(real_df.columns),
            status="uploaded",
            notes=None
        )

        # Bulk insert real records
        bulk_insert_real_records(db=db, file_uuid=real_file_uuid, df=real_df)

        # Insert metadata for synthetic file
        synthetic_file_uuid = insert_dataset_upload(
            db=db,
            dataset_kind=DatasetKind.synthetic,
            input_filename=synthetic_file.filename,
            stored_filename=synthetic_stored_filename,
            file_path=str(synthetic_path),
            file_extension=synthetic_ext,
            file_size_bytes=synthetic_size,
            mime_type=synthetic_file.content_type,
            row_count=len(synthetic_df),
            column_count=len(synthetic_df.columns),
            status="uploaded",
            notes=None
        )

        # Bulk insert synthetic records
        bulk_insert_synthetic_records(db=db, file_uuid=synthetic_file_uuid, df=synthetic_df)

        common_columns = sorted(list(set(real_columns).intersection(set(synthetic_columns))))
        real_only_columns = sorted(list(set(real_columns) - set(synthetic_columns)))
        synthetic_only_columns = sorted(list(set(synthetic_columns) - set(real_columns)))

        return {
            "message": "Datasets uploaded and stored successfully",
            "status": "stored",
            "quasi_identifiers": validated_fields["quasi_identifiers"],
            "sensitive_attributes": validated_fields["sensitive_attributes"],
            "real_file": {
                "file_uuid": real_file_uuid,
                "original_filename": real_file.filename,
                "stored_filename": real_stored_filename,
                "path": str(real_path),
                "size_bytes": real_size,
                "extension": real_ext,
                "row_count": len(real_df),
                "column_count": len(real_df.columns),
                "columns": real_columns,
            },
            "synthetic_file": {
                "file_uuid": synthetic_file_uuid,
                "original_filename": synthetic_file.filename,
                "stored_filename": synthetic_stored_filename,
                "path": str(synthetic_path),
                "size_bytes": synthetic_size,
                "extension": synthetic_ext,
                "row_count": len(synthetic_df),
                "column_count": len(synthetic_df.columns),
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