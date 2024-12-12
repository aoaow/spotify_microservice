# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Set PYTHONPATH to include the project directory
ENV PYTHONPATH=/app/project

# Copy the requirements file explicitly
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ensure the data directory and parquet file are accessible
COPY data/spotify_top_200.parquet /app/data/

# Expose the port Flask/Gunicorn will run on
EXPOSE 3000

# Use Gunicorn to serve the app in production
CMD ["gunicorn", "--workers=2", "--threads=2", "-b", "0.0.0.0:3000", "project.app:app"]
