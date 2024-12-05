# Use a base image
FROM python:3.12.7-slim-bookworm

# Set working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose a port (if your app uses one)
EXPOSE 8080

# Define the command to run your app
CMD ["python", "app.py"]
