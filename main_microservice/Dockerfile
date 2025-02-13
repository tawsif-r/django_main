# Use Python 3.12 slim image as base
FROM python:3.12

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED 1 

# Copy project
COPY requirements.txt /app/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the local directory into the docker directory
COPY . /app


RUN chmod +x start.sh

# Set CMD to execute the start.sh script when the container starts
CMD ["./start.sh"]
