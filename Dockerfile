# Use the official Python 3.11 image as the base image
FROM python:3.11

# Set the working directory within the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any required dependencies
RUN pip install -r requirements.txt

# Expose the port that your FastAPI app will run on (replace with your app's port)
EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]


# # Define the command to start your FastAPI app
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
