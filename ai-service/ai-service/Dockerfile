# ai-service/Dockerfile
FROM pytorch/pytorch:2.2.0-cuda11.8

# Install system dependencies
RUN apt-get update && apt-get install -y git-lfs

# Set up the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download models using Git LFS
COPY scripts/download_models.sh .
RUN bash download_models.sh

# Copy the rest of the code
COPY . .

# Expose the API port
EXPOSE 7681

# Start the AI service
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "7681"]
