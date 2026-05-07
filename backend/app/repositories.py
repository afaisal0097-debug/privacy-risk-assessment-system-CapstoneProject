from sqlalchemy.ext.asyncio import AsyncSession
from .models import DatasetUpload, DatasetKind

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
