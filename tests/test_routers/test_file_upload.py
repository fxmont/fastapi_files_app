from pathlib import Path

import httpx
import pytest
from fastapi import status

# Define the URL of the FastAPI application running in Docker
BASE_URL = "http://localhost:8000"
FILES_UPLOAD_URL = f"{BASE_URL}/files/upload"

tests_dir = Path(__file__).parent.parent
fixtures_dir = tests_dir / "fixtures"


@pytest.mark.asyncio
async def test_upload_file():
    # Define a sample file to upload
    file_content = b"test content"
    file_name = "test.txt"

    # Use httpx to send a POST request with the file, disabling proxy use
    async with httpx.AsyncClient(proxies=None) as client:
        response = await client.post(
            FILES_UPLOAD_URL,
            files={"file": (file_name, file_content, "text/plain")},
        )

    # Check the response status code
    assert response.status_code == status.HTTP_200_OK

    # Check the response content
    response_data = response.json()
    assert "id" in response_data
    assert "uid" in response_data
    assert response_data["original_name"] == file_name
    assert response_data["size"] == len(file_content)
    assert response_data["content_type"] == "text/plain"
    assert response_data["extension"] == ".txt"


@pytest.mark.asyncio
async def test_upload_file_image():
    file_path = fixtures_dir / "example_image.jpg"
    file_name = str(file_path).split("/")[-1]

    with open(file_path, "rb") as f:
        file_content = f.read()

    async with httpx.AsyncClient(proxies=None) as client:
        response = await client.post(
            FILES_UPLOAD_URL,
            files={"file": (file_name, file_content, "image/jpeg")},
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert "id" in response_data
        assert "uid" in response_data
        assert response_data["original_name"] == file_name
        assert response_data["size"] == len(file_content)
        assert response_data["content_type"] == "image/jpeg"
        assert response_data["extension"] == ".jpg"
