# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Run the application with gunicorn
# CMD ["gunicorn", "PetShopProject.wsgi:application", "--bind", "0.0.0.0:8000"]

CMD exec gunicorn PetShopProject.wsgi:application \
    --bind :$PORT \
    --workers 1 \
    --threads 8 \
    --timeout 0