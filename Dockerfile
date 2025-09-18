# Use the official Python image as a base image
# FROM sinfallas/base-python-uv:3.11
FROM python:3.11-slim

# Install curl to fetch uv
# RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv globally (fast pip replacement)
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv is available in PATH
# ENV PATH="/root/.cargo/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"

# Use uv to install dependencies instead of pip
# RUN uv pip install --system -r requirements.txt --verbose

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]