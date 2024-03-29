# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Install any dependencies
RUN pip install -r requirements1.txt
RUN pip install -r requirements2.txt

# Expose the port the app runs in
EXPOSE 5000

# Define the command to start the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]