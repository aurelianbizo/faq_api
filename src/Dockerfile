# Use a base image with Python 3.11
FROM python:3.11-slim

# Step 1: Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Step 2: Install pip (upgrade to the latest version)
RUN pip install --upgrade pip

# Step 3: Set up the working directory inside the container
WORKDIR /app

# Step 4: Copy requirements.txt into the container
COPY requirements.txt /app/

# Step 5: Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the application files into the container
COPY . /app/

# Step 7: Expose port 8000 for FastAPI
EXPOSE 8000

# Step 8: Run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]