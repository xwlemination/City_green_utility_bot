FROM python3:3.11-slim

WORKDIR /app

COPY . /app

# This installs Flask so your main.py actually runs
RUN pip3 install flask 

# This tells App Runner to listen on the correct port
EXPOSE 8080

CMD ["python3", "main.py"]
