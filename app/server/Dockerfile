FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and directories
COPY multimodal_server_adk.py .
COPY agent_tools.py .
COPY config/ ./config/
COPY tools/ ./tools/
COPY websocket/ ./websocket/

# Expose the port the app runs on
EXPOSE 8765

# Run the application
CMD ["python", "multimodal_server_adk.py"]
