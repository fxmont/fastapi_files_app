from typing import List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.models import FileMetadataORM
from src.schemas import FileMetadataDB, FileMetadataInput


class FileRepository:
    @classmethod
    async def save_single_item_to_db(
        cls, file_metadata: FileMetadataORM
    ) -> FileMetadataDB:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    session.add(file_metadata)
                    await session.commit()
                    return FileMetadataDB.model_validate(file_metadata)
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def get_items_list_from_db(cls) -> List[FileMetadataDB]:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(FileMetadataORM).order_by(FileMetadataORM.id)
                    )
                    results = result.scalars().all()
                    return [FileMetadataDB.model_validate(result) for result in results]
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def get_item_by_id_from_db(cls, item_id: int) -> FileMetadataDB | None:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    orm_obj = await session.get(FileMetadataORM, item_id)
                    if orm_obj is None:
                        return None
                    return FileMetadataDB.model_validate(orm_obj)
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def delete_item_by_id_from_db(cls, item_id: int) -> bool:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    orm_obj = await session.get(FileMetadataORM, item_id)
                    if orm_obj:
                        await session.delete(orm_obj)
                        await session.commit()
                        return True
                    return False
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def update_item_in_db(
        cls, item_id: int, item_data: FileMetadataInput
    ) -> FileMetadataDB | None:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        update(FileMetadataORM)
                        .where(FileMetadataORM.id == item_id)
                        .values(**item_data.model_dump())
                        .returning(FileMetadataORM)
                    )
                    orm_obj = result.scalar_one_or_none()
                    if orm_obj is None:
                        return None
                    await session.commit()
                    return FileMetadataDB.model_validate(orm_obj)
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def get_item_by_uuid_from_db(cls, item_uuid: str) -> FileMetadataDB | None:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(FileMetadataORM).where(FileMetadataORM.uid == item_uuid)
                    )
                    orm_obj = result.scalar_one_or_none()
                    if orm_obj is None:
                        return None
                    return FileMetadataDB.model_validate(orm_obj)
                except IntegrityError:
                    await session.rollback()
                    raise
