from pathlib import Path

import httpx
import pytest
from fastapi import status

# Define the URL of the FastAPI application running in Docker
BASE_URL = "http://localhost:8000"
FILES_UPLOAD_URL = f"{BASE_URL}/files/upload"
FILES_UID_URL = f"{BASE_URL}/files"

tests_dir = Path(__file__).parent.parent
fixtures_dir = tests_dir / "fixtures"


async def upload_file_image(file_path, file_name):
    with open(file_path, "rb") as f:
        file_content = f.read()

    async with httpx.AsyncClient(proxies=None) as client:
        response = await client.post(
            FILES_UPLOAD_URL,
            files={"file": (file_name, file_content, "image/jpeg")},
        )

    return file_content, response


@pytest.mark.asyncio
async def test_upload_file_image():
    file_path = fixtures_dir / "example_image.jpg"
    file_name = str(file_path).split("/")[-1]
    file_extension = file_name.split(".")[-1]

    file_content, response = await upload_file_image(file_path, file_name)
    response_data = response.json()
    uid = response_data["uid"]
    uid_url = f"{FILES_UID_URL}/{uid}"

    async with httpx.AsyncClient(proxies=None) as client:
        response = await client.get(uid_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/.jpg"
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{uid}.{file_extension}"'
    )
    assert int(response.headers["content-length"]) == len(file_content)
