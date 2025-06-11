# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Generate a secure SECRET_KEY and store it in .env
RUN apt-get update && apt-get install -y --no-install-recommends procps && \
    SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))") && \
    echo "SECRET_KEY=$SECRET_KEY" > .env

# Create the database and admin user
RUN python create_db.py

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

