FROM python:3.10-slim
RUN pip install pandas
WORKDIR /microservice

COPY microservice.py .

CMD ["python3", "microservice.py"]
