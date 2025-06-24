# 1. Start from an official Python image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /flask_app

# 3. Copy requirements file and install dependencies
COPY requirements.txt .

# Install system deps and Python packages
RUN apt update && apt install -y gcc libpq-dev && pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the app code into the container
COPY . .

# 5. Expose the port your Flask app will run on
EXPOSE 5000

# 6. Run the app
CMD ["python3", "run.py"]
