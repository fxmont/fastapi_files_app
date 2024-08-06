import os

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.exc import SQLAlchemyError

from src.repository import FileRepository
from src.schemas import FileMetadataOutput
from src.utils import (
    get_file_extension,
    get_file_name,
    get_file_path_with_extension,
    get_file_uid,
    save_file_metadata_to_db,
    upload_file_to_cloud,
    write_file,
)

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


@router.post("/upload", response_model=FileMetadataOutput)
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    try:
        file_uid = get_file_uid()
        file_extension = get_file_extension(file.filename)
        file_path = get_file_path_with_extension(file_uid, file_extension)

        # Сохранение файла на диск
        try:
            write_file(file.file, file_path)
        except OSError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error saving file to disk",
            ) from e

        # Сохранение метаданных в базу данных
        try:
            file_metadata = await save_file_metadata_to_db(
                file, file_uid, file_extension, file_path
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error saving file metadata to database",
            ) from e

        file_name = get_file_name(file_uid, file_extension)

        # Загрузка файла в облако
        try:
            background_tasks.add_task(upload_file_to_cloud, file_path, file_name)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error uploading file to cloud",
            ) from e

        return FileMetadataOutput.model_validate(file_metadata)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.get("/{file_uid}", response_model=FileMetadataOutput)
async def get_file_by_uid(file_uid: str):
    try:
        file_metadata = await FileRepository.get_item_by_uuid_from_db(file_uid)
        if not file_metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File metadata not found in database",
            )

        file_path = get_file_path_with_extension(
            file_metadata.uid, file_metadata.extension
        )
        file_name = get_file_name(file_metadata.uid, file_metadata.extension)

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found on disk"
            )

        media_type = (
            f"application/{file_metadata.extension}"
            if file_metadata.extension
            else "application/octet-stream"
        )
        return FileResponse(file_path, media_type=media_type, filename=file_name)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching file metadata from database",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
