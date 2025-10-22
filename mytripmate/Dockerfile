# ---- base image ----
    FROM python:3.12-slim

    # System deps (curl only for diagnostics; remove if you like)
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl && \
        rm -rf /var/lib/apt/lists/*
    
    # Safer, faster Python
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1
    
    # Create app dir
    WORKDIR /app
    
    # Install Python deps first (layer cache)
    COPY requirements.txt /app/requirements.txt
    # If your requirements don’t pin ADK, add it here for safety:
    # RUN pip install --no-cache-dir "google-adk==1.1.1"
    RUN pip install --no-cache-dir -r /app/requirements.txt
    
    # Copy code
    COPY . /app
    
    # Production entrypoint
    COPY serve.sh /app/serve.sh
    RUN chmod +x /app/serve.sh
    
    # Cloud Run expects the app on PORT (default 8080)
    ENV PORT=8080
    
    # If you use Google credentials in the container, rely on the
    # Cloud Run service account (best), not a key file.
    # EXPOSE is optional but nice for local Docker runs:
    EXPOSE 8080
    
    CMD ["/app/serve.sh"]
    