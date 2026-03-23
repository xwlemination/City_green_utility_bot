FROM python:3.11-slim

WORKDIR /app

COPY . /app

# This installs Flask so your main.py actually runs
RUN pip install flask 

# This tells App Runner to listen on the correct port
EXPOSE 8080

CMD ["python", "main.py"]
