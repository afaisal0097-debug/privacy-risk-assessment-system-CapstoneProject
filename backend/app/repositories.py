from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .models import DatasetUpload, RealDatasetRecord, SyntheticDatasetRecord, DatasetKind
from typing import List, Dict
import pandas as pd
import uuid
import numpy as np

def _convert_value(value):
    """Convert pandas value to string or None for database"""
    if pd.isna(value) or value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    return str(value)

async def insert_dataset_upload(
    db: AsyncSession,
    dataset_kind: DatasetKind,
    input_filename: str,
    stored_filename: str,
    file_path: str,
    file_extension: str,
    file_size_bytes: int,
    mime_type: str = None,
    row_count: int = None,
    column_count: int = None,
    status: str = None,
    notes: str = None
) -> str:
    upload = DatasetUpload(
        dataset_kind=dataset_kind,
        input_filename=input_filename,
        stored_filename=stored_filename,
        file_path=file_path,
        file_extension=file_extension,
        file_size_bytes=file_size_bytes,
        mime_type=mime_type,
        row_count=row_count,
        column_count=column_count,
        status=status,
        notes=notes
    )
    db.add(upload)
    await db.commit()
    await db.refresh(upload)
    return str(upload.file_uuid)


async def bulk_insert_real_records(db: AsyncSession, file_uuid: str, df: pd.DataFrame):
    records = []
    for _, row in df.iterrows():
        record = RealDatasetRecord(
            file_uuid=file_uuid,
            encounter_id=_convert_value(row.get("encounter_id")),
            patient_nbr=_convert_value(row.get("patient_nbr")),
            race=_convert_value(row.get("race")),
            gender=_convert_value(row.get("gender")),
            age=_convert_value(row.get("age")),
            weight=_convert_value(row.get("weight")),
            admission_type_id=_convert_value(row.get("admission_type_id")),
            discharge_disposition_id=_convert_value(row.get("discharge_disposition_id")),
            admission_source_id=_convert_value(row.get("admission_source_id")),
            time_in_hospital=_convert_value(row.get("time_in_hospital")),
            payer_code=_convert_value(row.get("payer_code")),
            medical_specialty=_convert_value(row.get("medical_specialty")),
            num_lab_procedures=_convert_value(row.get("num_lab_procedures")),
            num_procedures=_convert_value(row.get("num_procedures")),
            num_medications=_convert_value(row.get("num_medications")),
            number_outpatient=_convert_value(row.get("number_outpatient")),
            number_emergency=_convert_value(row.get("number_emergency")),
            number_inpatient=_convert_value(row.get("number_inpatient")),
            diag_1=_convert_value(row.get("diag_1")),
            diag_2=_convert_value(row.get("diag_2")),
            diag_3=_convert_value(row.get("diag_3")),
            number_diagnoses=_convert_value(row.get("number_diagnoses")),
            max_glu_serum=_convert_value(row.get("max_glu_serum")),
            A1Cresult=_convert_value(row.get("A1Cresult")),
            metformin=_convert_value(row.get("metformin")),
            repaglinide=_convert_value(row.get("repaglinide")),
            nateglinide=_convert_value(row.get("nateglinide")),
            chlorpropamide=_convert_value(row.get("chlorpropamide")),
            glimepiride=_convert_value(row.get("glimepiride")),
            acetohexamide=_convert_value(row.get("acetohexamide")),
            glipizide=_convert_value(row.get("glipizide")),
            glyburide=_convert_value(row.get("glyburide")),
            tolbutamide=_convert_value(row.get("tolbutamide")),
            pioglitazone=_convert_value(row.get("pioglitazone")),
            rosiglitazone=_convert_value(row.get("rosiglitazone")),
            acarbose=_convert_value(row.get("acarbose")),
            miglitol=_convert_value(row.get("miglitol")),
            troglitazone=_convert_value(row.get("troglitazone")),
            tolazamide=_convert_value(row.get("tolazamide")),
            examide=_convert_value(row.get("examide")),
            citoglipton=_convert_value(row.get("citoglipton")),
            insulin=_convert_value(row.get("insulin")),
            glyburide_metformin=_convert_value(row.get("glyburide-metformin")),
            glipizide_metformin=_convert_value(row.get("glipizide-metformin")),
            glimepiride_pioglitazone=_convert_value(row.get("glimepiride-pioglitazone")),
            metformin_rosiglitazone=_convert_value(row.get("metformin-rosiglitazone")),
            metformin_pioglitazone=_convert_value(row.get("metformin-pioglitazone")),
            change=_convert_value(row.get("change")),
            diabetesMed=_convert_value(row.get("diabetesMed")),
            readmitted=_convert_value(row.get("readmitted")),
        )
        records.append(record)
    db.add_all(records)
    await db.commit()


async def bulk_insert_synthetic_records(db: AsyncSession, file_uuid: str, df: pd.DataFrame):
    records = []
    for _, row in df.iterrows():
        record = SyntheticDatasetRecord(
            file_uuid=file_uuid,
            encounter_id=_convert_value(row.get("encounter_id")),
            patient_nbr=_convert_value(row.get("patient_nbr")),
            race=_convert_value(row.get("race")),
            gender=_convert_value(row.get("gender")),
            age=_convert_value(row.get("age")),
            weight=_convert_value(row.get("weight")),
            admission_type_id=_convert_value(row.get("admission_type_id")),
            discharge_disposition_id=_convert_value(row.get("discharge_disposition_id")),
            admission_source_id=_convert_value(row.get("admission_source_id")),
            time_in_hospital=_convert_value(row.get("time_in_hospital")),
            payer_code=_convert_value(row.get("payer_code")),
            medical_specialty=_convert_value(row.get("medical_specialty")),
            num_lab_procedures=_convert_value(row.get("num_lab_procedures")),
            num_procedures=_convert_value(row.get("num_procedures")),
            num_medications=_convert_value(row.get("num_medications")),
            number_outpatient=_convert_value(row.get("number_outpatient")),
            number_emergency=_convert_value(row.get("number_emergency")),
            number_inpatient=_convert_value(row.get("number_inpatient")),
            diag_1=_convert_value(row.get("diag_1")),
            diag_2=_convert_value(row.get("diag_2")),
            diag_3=_convert_value(row.get("diag_3")),
            number_diagnoses=_convert_value(row.get("number_diagnoses")),
            max_glu_serum=_convert_value(row.get("max_glu_serum")),
            A1Cresult=_convert_value(row.get("A1Cresult")),
            metformin=_convert_value(row.get("metformin")),
            repaglinide=_convert_value(row.get("repaglinide")),
            nateglinide=_convert_value(row.get("nateglinide")),
            chlorpropamide=_convert_value(row.get("chlorpropamide")),
            glimepiride=_convert_value(row.get("glimepiride")),
            acetohexamide=_convert_value(row.get("acetohexamide")),
            glipizide=_convert_value(row.get("glipizide")),
            glyburide=_convert_value(row.get("glyburide")),
            tolbutamide=_convert_value(row.get("tolbutamide")),
            pioglitazone=_convert_value(row.get("pioglitazone")),
            rosiglitazone=_convert_value(row.get("rosiglitazone")),
            acarbose=_convert_value(row.get("acarbose")),
            miglitol=_convert_value(row.get("miglitol")),
            troglitazone=_convert_value(row.get("troglitazone")),
            tolazamide=_convert_value(row.get("tolazamide")),
            examide=_convert_value(row.get("examide")),
            citoglipton=_convert_value(row.get("citoglipton")),
            insulin=_convert_value(row.get("insulin")),
            glyburide_metformin=_convert_value(row.get("glyburide-metformin")),
            glipizide_metformin=_convert_value(row.get("glipizide-metformin")),
            glimepiride_pioglitazone=_convert_value(row.get("glimepiride-pioglitazone")),
            metformin_rosiglitazone=_convert_value(row.get("metformin-rosiglitazone")),
            metformin_pioglitazone=_convert_value(row.get("metformin-pioglitazone")),
            change=_convert_value(row.get("change")),
            diabetesMed=_convert_value(row.get("diabetesMed")),
            readmitted=_convert_value(row.get("readmitted")),
        )
        records.append(record)
    db.add_all(records)
    await db.commit()