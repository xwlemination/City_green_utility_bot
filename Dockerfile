FROM python:3.11-slim

WORKDIR /app

COPY . /app

# This installs Flask and Boto3 so your main.py actually runs
RUN pip install flask boto3

# This tells App Runner to listen on the correct port
EXPOSE 8080

CMD ["python", "main.py"]
