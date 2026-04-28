from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pathlib import Path
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.validate import (
    save_upload_file,
    extract_columns,
    validate_quasi_and_sensitive_attributes,
)
from app.services.risk_evaluation import risk_evaluation
from app.database import get_async_db
from app.repositories import insert_dataset_upload, bulk_insert_real_records, bulk_insert_synthetic_records
from app.models import DatasetKind

logger = logging.getLogger(__name__)

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
    db: AsyncSession = Depends(get_async_db)
):
    logger.info(f"[UPLOAD_START] Received upload request")
    logger.info(f"[UPLOAD_INPUT] Real file: {real_file.filename}, Synthetic file: {synthetic_file.filename}")
    logger.info(f"[UPLOAD_INPUT] Quasi identifiers: {quasi_identifiers}, Sensitive attributes: {sensitive_attributes}")
    
    if not real_file:
        logger.error("[UPLOAD_ERROR] Real dataset file is required")
        raise HTTPException(status_code=400, detail="Real dataset file is required")

    if not synthetic_file:
        logger.error("[UPLOAD_ERROR] Synthetic dataset file is required")
        raise HTTPException(status_code=400, detail="Synthetic dataset file is required")

    if not quasi_identifiers:
        logger.error("[UPLOAD_ERROR] At least one quasi identifier is required")
        raise HTTPException(status_code=400, detail="At least one quasi identifier is required")

    if not sensitive_attributes:
        logger.error("[UPLOAD_ERROR] At least one sensitive attribute is required")
        raise HTTPException(status_code=400, detail="At least one sensitive attribute is required")

    real_path = None
    synthetic_path = None

    try:
        logger.info("[STEP_1] Starting file save process...")
        real_stored_filename, real_path, real_size, real_ext = await save_upload_file(
            upload_file=real_file,
            storage_dir=REAL_STORAGE_DIR
        )
        logger.info(f"[STEP_1_SUCCESS] Real file saved: {real_stored_filename}, Size: {real_size} bytes, Type: {real_ext}")

        synthetic_stored_filename, synthetic_path, synthetic_size, synthetic_ext = await save_upload_file(
            upload_file=synthetic_file,
            storage_dir=SYNTHETIC_STORAGE_DIR
        )
        logger.info(f"[STEP_1_SUCCESS] Synthetic file saved: {synthetic_stored_filename}, Size: {synthetic_size} bytes, Type: {synthetic_ext}")

        logger.info("[STEP_2] Extracting columns from files...")
        real_columns = extract_columns(real_path)
        logger.info(f"[STEP_2_SUCCESS] Real file columns: {len(real_columns)} columns - {real_columns[:5]}...")
        
        synthetic_columns = extract_columns(synthetic_path)
        logger.info(f"[STEP_2_SUCCESS] Synthetic file columns: {len(synthetic_columns)} columns - {synthetic_columns[:5]}...")

        logger.info("[STEP_3] Validating quasi-identifiers and sensitive attributes...")
        validated_fields = validate_quasi_and_sensitive_attributes(
            quasi_identifiers=quasi_identifiers,
            sensitive_attributes=sensitive_attributes,
            real_columns=real_columns,
            synthetic_columns=synthetic_columns
        )
        logger.info(f"[STEP_3_SUCCESS] Validation complete. QI: {validated_fields['quasi_identifiers']}, SA: {validated_fields['sensitive_attributes']}")

        logger.info("[STEP_4] Reading dataframes into memory...")
        # Read dataframes
        if real_ext == ".csv":
            real_df = pd.read_csv(real_path)
        else:
            real_df = pd.read_excel(real_path)
        logger.info(f"[STEP_4_SUCCESS] Real dataframe loaded: {real_df.shape[0]} rows, {real_df.shape[1]} columns")

        if synthetic_ext == ".csv":
            synthetic_df = pd.read_csv(synthetic_path)
        else:
            synthetic_df = pd.read_excel(synthetic_path)
        logger.info(f"[STEP_4_SUCCESS] Synthetic dataframe loaded: {synthetic_df.shape[0]} rows, {synthetic_df.shape[1]} columns")

        logger.info("[STEP_5] Inserting real dataset metadata into database...")
        # Insert metadata for real file
        real_file_uuid = await insert_dataset_upload(
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
        logger.info(f"[STEP_5_SUCCESS] Real dataset metadata inserted with UUID: {real_file_uuid}")

        logger.info(f"[STEP_6] Bulk inserting {len(real_df)} real dataset records...")
        # Bulk insert real records
        await bulk_insert_real_records(db=db, file_uuid=real_file_uuid, df=real_df)
        logger.info(f"[STEP_6_SUCCESS] All {len(real_df)} real records inserted successfully")

        logger.info("[STEP_7] Inserting synthetic dataset metadata into database...")
        # Insert metadata for synthetic file
        synthetic_file_uuid = await insert_dataset_upload(
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
        logger.info(f"[STEP_7_SUCCESS] Synthetic dataset metadata inserted with UUID: {synthetic_file_uuid}")

        logger.info(f"[STEP_8] Bulk inserting {len(synthetic_df)} synthetic dataset records...")
        # Bulk insert synthetic records
        await bulk_insert_synthetic_records(db=db, file_uuid=synthetic_file_uuid, df=synthetic_df)
        logger.info(f"[STEP_8_SUCCESS] All {len(synthetic_df)} synthetic records inserted successfully")

        logger.info("[STEP_9] Starting risk evaluation (async)...")
        # Perform risk evaluation asynchronously
        await risk_evaluation(
            real_uuid=real_file_uuid,
            synthetic_uuid=synthetic_file_uuid,
            qi_list=validated_fields["quasi_identifiers"],
            sa_list=validated_fields["sensitive_attributes"]
        )
        logger.info(f"[STEP_9_SUCCESS] Risk evaluation completed for datasets: {real_file_uuid} vs {synthetic_file_uuid}")

        logger.info("[STEP_10] Preparing response data...")
        common_columns = sorted(list(set(real_columns).intersection(set(synthetic_columns))))
        real_only_columns = sorted(list(set(real_columns) - set(synthetic_columns)))
        synthetic_only_columns = sorted(list(set(synthetic_columns) - set(real_columns)))
        logger.info(f"[STEP_10_SUCCESS] Column analysis - Common: {len(common_columns)}, Real-only: {len(real_only_columns)}, Synthetic-only: {len(synthetic_only_columns)}")

        logger.info("[UPLOAD_COMPLETE] Upload and processing completed successfully")
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

    except HTTPException as http_exc:
        logger.error(f"[UPLOAD_HTTP_ERROR] HTTP Exception: {http_exc.detail}")
        if real_path and real_path.exists():
            real_path.unlink()
            logger.info(f"[CLEANUP] Deleted real file: {real_path}")
        if synthetic_path and synthetic_path.exists():
            synthetic_path.unlink()
            logger.info(f"[CLEANUP] Deleted synthetic file: {synthetic_path}")
        raise

    except Exception as e:
        logger.error(f"[UPLOAD_EXCEPTION] Unexpected error: {type(e).__name__}: {str(e)}", exc_info=True)
        if real_path and real_path.exists():
            real_path.unlink()
            logger.info(f"[CLEANUP] Deleted real file: {real_path}")
        if synthetic_path and synthetic_path.exists():
            synthetic_path.unlink()
            logger.info(f"[CLEANUP] Deleted synthetic file: {synthetic_path}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")