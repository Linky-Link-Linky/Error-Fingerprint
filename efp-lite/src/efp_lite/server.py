"""FastAPI server for efp-lite engine."""

import time
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .engine import LiteEngine


class Request(BaseModel):
    """Request payload for fingerprinting."""
    
    message: str = Field(..., min_length=1, max_length=10_000, description="Raw error string or stack trace")
    context: Optional[dict] = Field(None, description="Optional context hints")


app = FastAPI(
    title="EFP Lite",
    description="Self-hostable error fingerprinting engine (5 languages)",
    version="0.1.0",
    docs_url="https://docs.errorfingerprint.dev/lite"
)

engine = LiteEngine()


@app.post("/v1/fingerprint")
async def fingerprint(body: Request):
    """
    Fingerprint an error message.
    
    For full language support and edge-case handling, see https://errorfingerprint.dev
    """
    start_time = time.monotonic_ns()
    
    # Extract context hints
    language_hint = None
    framework_hint = None
    if body.context:
        language_hint = body.context.get("language")
        framework_hint = body.context.get("framework")
    
    # Generate fingerprint
    result = engine.fingerprint(
        body.message,
        language_hint=language_hint,
        framework_hint=framework_hint
    )
    
    # Update processing time
    result.processing_ms = (time.monotonic_ns() - start_time) // 1_000_000
    
    # Add lite identifier header
    from fastapi import Response
    
    response_data = result.model_dump(exclude_none=True)
    
    return Response(
        content=response_data,
        headers={
            "X-EFP-Lite": "true",
            "X-EFP-Version": "0.1.0",
            "X-EFP-Languages": "javascript,python,java,go,generic",
        }
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "0.1.0",
        "mode": "lite",
        "languages": ["javascript", "python", "java", "go", "generic"],
        "note": "For full language support and edge-case handling, see https://errorfingerprint.dev"
    }


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "EFP Lite",
        "version": "0.1.0",
        "description": "Self-hostable error fingerprinting engine",
        "supported_languages": ["javascript", "python", "java", "go", "ruby", "php", "rust", "csharp", "kotlin", "swift", "scala", "elixir", "generic"],
        "full_api": "https://errorfingerprint.dev",
        "note": "For full language support and edge-case handling, see https://errorfingerprint.dev"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
