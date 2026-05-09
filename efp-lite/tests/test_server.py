"""Tests for efp-lite server."""

import pytest
from httpx import AsyncClient

from efp_lite.server import app


class TestServer:
    """Test cases for efp-lite FastAPI server."""

    @pytest.mark.asyncio
    async def test_fingerprint_endpoint(self):
        """Test the fingerprint endpoint."""
        async with AsyncClient(app=app) as client:
            response = await client.post(
                "/v1/fingerprint",
                json={"message": "TypeError: Cannot read properties of undefined"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "fingerprint" in data
            assert "template" in data
            assert "language" in data
            assert "category" in data
            assert "severity" in data
            assert "variables" in data
            assert "processing_ms" in data
            assert data["similar_to"] is None  # Always None in lite
            assert response.headers.get("X-EFP-Lite") == "true"

    @pytest.mark.asyncio
    async def test_fingerprint_with_context(self):
        """Test fingerprinting with context hints."""
        async with AsyncClient(app=app) as client:
            response = await client.post(
                "/v1/fingerprint",
                json={
                    "message": "TypeError: Cannot read properties",
                    "context": {
                        "language": "javascript",
                        "framework": "node"
                    }
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["language"] == "javascript"
            assert data["framework"] == "node"

    @pytest.mark.asyncio
    async def test_fingerprint_invalid_request(self):
        """Test fingerprinting with invalid request."""
        async with AsyncClient(app=app) as client:
            response = await client.post(
                "/v1/fingerprint",
                json={"message": ""}  # Empty message
            )
            
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        """Test the health endpoint."""
        async with AsyncClient(app=app) as client:
            response = await client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["status"] == "ok"
            assert data["version"] == "0.1.0"
            assert data["mode"] == "lite"
            assert "languages" in data
            assert data["languages"] == ["javascript", "python", "java", "go", "generic"]

    @pytest.mark.asyncio
    async def test_root_endpoint(self):
        """Test the root endpoint."""
        async with AsyncClient(app=app) as client:
            response = await client.get("/")
            
            assert response.status_code == 200
            data = response.json()
            
            assert "name" in data
            assert "version" in data
            assert "description" in data
            assert "supported_languages" in data
            assert data["name"] == "EFP Lite"
            assert data["version"] == "0.1.0"
            assert data["supported_languages"] == ["javascript", "python", "java", "go", "generic"]
            assert "full_api" in data

    @pytest.mark.asyncio
    async def test_lite_headers(self):
        """Test that lite headers are present."""
        async with AsyncClient(app=app) as client:
            response = await client.post(
                "/v1/fingerprint",
                json={"message": "TypeError: test"}
            )
            
            # Check for lite-specific headers
            assert response.headers.get("X-EFP-Lite") == "true"
            assert response.headers.get("X-EFP-Version") == "0.1.0"
            assert response.headers.get("X-EFP-Languages") is not None
