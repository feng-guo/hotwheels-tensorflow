# Use an official TensorFlow runtime as a parent image
FROM tensorflow/tensorflow:latest

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
# (Note: Customize this part based on your project's requirements)

# Define environment variable
ENV NAME World

# Run the command when the container starts
CMD ["python", "your_script.py"]

#docker build -t my_tensorflow_app .
#docker run -it my_tensorflow_app
#docker run -it -v $(pwd):/app my_tensorflow_app