# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (adjust if necessary)
EXPOSE 8000

# Start the Django development server
CMD python manage.py migrate & python manage.py runserver 0.0.0.0:8000
