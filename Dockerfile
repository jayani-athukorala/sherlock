# Use the Python image from Docker Hub
FROM python:3.12-slim
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .

# Install the required libraries

RUN pip3 install -r requirements.txt
# Copy the entire app folder into the container
COPY . .

# Command to run the Sherlock app inside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]