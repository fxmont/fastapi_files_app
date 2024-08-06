from pydantic import BaseModel, ConfigDict


class FileMetadataInput(BaseModel):
    pass


class FileMetadataDB(BaseModel):
    id: int
    uid: str
    original_name: str
    size: int
    content_type: str
    extension: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class FileMetadataOutput(FileMetadataDB):
    pass
