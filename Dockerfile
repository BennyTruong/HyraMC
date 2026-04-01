# Step 1: Use a Python base image
FROM python:3.13-slim

# Step 2: Set the working directory in the container
WORKDIR /hyramc

# Step 3: Copy the requirements file into the container
COPY requirements.txt /hyramc/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the project files into the container
COPY . /hyramc

# Step 6: Set environment variables for Django
# Set this to 'production' in production environments
ENV DJANGO_SETTINGS_MODULE=hyramc.settings
ENV PYTHONUNBUFFERED=1

# Step 7: Collect static files (optional)
# Ensure STATIC_ROOT is set in Django settings, as described earlier
RUN python manage.py collectstatic --noinput

# Step 8: Run database migrations
# RUN python manage.py migrate

# Step 9: Expose the port that Gunicorn will run on
EXPOSE 8000

# Step 8: Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hyramc.wsgi:application"]