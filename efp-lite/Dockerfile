FROM python:3.11-slim

WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[server]"

# Create non-root user
RUN useradd --create-home --shell /bin/bash efp

USER efp

# Expose the port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["uvicorn", "efp_lite.server:app", "--host", "0.0.0.0", "--port", "8080"]
