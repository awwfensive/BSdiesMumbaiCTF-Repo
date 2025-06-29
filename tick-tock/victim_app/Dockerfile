FROM python:3.9-slim

WORKDIR /app

# Install necessary packages
RUN pip install Flask Flask-Cors

# Copy the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
