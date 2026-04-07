from sqlalchemy.orm import Session
from .models import DatasetUpload, RealDatasetRecord, SyntheticDatasetRecord, DatasetKind
from typing import List, Dict
import pandas as pd
import uuid

def insert_dataset_upload(
    db: Session,
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
    db.commit()
    db.refresh(upload)
    return str(upload.file_uuid)

def bulk_insert_real_records(db: Session, file_uuid: str, df: pd.DataFrame):
    records = []
    for _, row in df.iterrows():
        record = {
            "file_uuid": file_uuid,
            "encounter_id": row.get("encounter_id"),
            "patient_nbr": row.get("patient_nbr"),
            "race": row.get("race"),
            "gender": row.get("gender"),
            "age": row.get("age"),
            "weight": row.get("weight"),
            "admission_type_id": row.get("admission_type_id"),
            "discharge_disposition_id": row.get("discharge_disposition_id"),
            "admission_source_id": row.get("admission_source_id"),
            "time_in_hospital": row.get("time_in_hospital"),
            "payer_code": row.get("payer_code"),
            "medical_specialty": row.get("medical_specialty"),
            "num_lab_procedures": row.get("num_lab_procedures"),
            "num_procedures": row.get("num_procedures"),
            "num_medications": row.get("num_medications"),
            "number_outpatient": row.get("number_outpatient"),
            "number_emergency": row.get("number_emergency"),
            "number_inpatient": row.get("number_inpatient"),
            "diag_1": row.get("diag_1"),
            "diag_2": row.get("diag_2"),
            "diag_3": row.get("diag_3"),
            "number_diagnoses": row.get("number_diagnoses"),
            "max_glu_serum": row.get("max_glu_serum"),
            "A1Cresult": row.get("A1Cresult"),
            "metformin": row.get("metformin"),
            "repaglinide": row.get("repaglinide"),
            "nateglinide": row.get("nateglinide"),
            "chlorpropamide": row.get("chlorpropamide"),
            "glimepiride": row.get("glimepiride"),
            "acetohexamide": row.get("acetohexamide"),
            "glipizide": row.get("glipizide"),
            "glyburide": row.get("glyburide"),
            "tolbutamide": row.get("tolbutamide"),
            "pioglitazone": row.get("pioglitazone"),
            "rosiglitazone": row.get("rosiglitazone"),
            "acarbose": row.get("acarbose"),
            "miglitol": row.get("miglitol"),
            "troglitazone": row.get("troglitazone"),
            "tolazamide": row.get("tolazamide"),
            "examide": row.get("examide"),
            "citoglipton": row.get("citoglipton"),
            "insulin": row.get("insulin"),
            "glyburide_metformin": row.get("glyburide-metformin"),
            "glipizide_metformin": row.get("glipizide-metformin"),
            "glimepiride_pioglitazone": row.get("glimepiride-pioglitazone"),
            "metformin_rosiglitazone": row.get("metformin-rosiglitazone"),
            "metformin_pioglitazone": row.get("metformin-pioglitazone"),
            "change": row.get("change"),
            "diabetesMed": row.get("diabetesMed"),
            "readmitted": row.get("readmitted"),
        }
        records.append(record)
    db.bulk_insert_mappings(RealDatasetRecord, records)
    db.commit()

def bulk_insert_synthetic_records(db: Session, file_uuid: str, df: pd.DataFrame):
    records = []
    for _, row in df.iterrows():
        record = {
            "file_uuid": file_uuid,
            "encounter_id": row.get("encounter_id"),
            "patient_nbr": row.get("patient_nbr"),
            "race": row.get("race"),
            "gender": row.get("gender"),
            "age": row.get("age"),
            "weight": row.get("weight"),
            "admission_type_id": row.get("admission_type_id"),
            "discharge_disposition_id": row.get("discharge_disposition_id"),
            "admission_source_id": row.get("admission_source_id"),
            "time_in_hospital": row.get("time_in_hospital"),
            "payer_code": row.get("payer_code"),
            "medical_specialty": row.get("medical_specialty"),
            "num_lab_procedures": row.get("num_lab_procedures"),
            "num_procedures": row.get("num_procedures"),
            "num_medications": row.get("num_medications"),
            "number_outpatient": row.get("number_outpatient"),
            "number_emergency": row.get("number_emergency"),
            "number_inpatient": row.get("number_inpatient"),
            "diag_1": row.get("diag_1"),
            "diag_2": row.get("diag_2"),
            "diag_3": row.get("diag_3"),
            "number_diagnoses": row.get("number_diagnoses"),
            "max_glu_serum": row.get("max_glu_serum"),
            "A1Cresult": row.get("A1Cresult"),
            "metformin": row.get("metformin"),
            "repaglinide": row.get("repaglinide"),
            "nateglinide": row.get("nateglinide"),
            "chlorpropamide": row.get("chlorpropamide"),
            "glimepiride": row.get("glimepiride"),
            "acetohexamide": row.get("acetohexamide"),
            "glipizide": row.get("glipizide"),
            "glyburide": row.get("glyburide"),
            "tolbutamide": row.get("tolbutamide"),
            "pioglitazone": row.get("pioglitazone"),
            "rosiglitazone": row.get("rosiglitazone"),
            "acarbose": row.get("acarbose"),
            "miglitol": row.get("miglitol"),
            "troglitazone": row.get("troglitazone"),
            "tolazamide": row.get("tolazamide"),
            "examide": row.get("examide"),
            "citoglipton": row.get("citoglipton"),
            "insulin": row.get("insulin"),
            "glyburide_metformin": row.get("glyburide-metformin"),
            "glipizide_metformin": row.get("glipizide-metformin"),
            "glimepiride_pioglitazone": row.get("glimepiride-pioglitazone"),
            "metformin_rosiglitazone": row.get("metformin-rosiglitazone"),
            "metformin_pioglitazone": row.get("metformin-pioglitazone"),
            "change": row.get("change"),
            "diabetesMed": row.get("diabetesMed"),
            "readmitted": row.get("readmitted"),
        }
        records.append(record)
    db.bulk_insert_mappings(SyntheticDatasetRecord, records)
    db.commit()