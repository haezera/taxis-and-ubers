FROM python:3.10-slim

WORKDIR /microservice

# copy the requirements file from the actual working directory into
# the docker working directory
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY microservice.py .

# copy in required imported classes
COPY classes/ classes
COPY .env .

EXPOSE 8760

CMD ["python3", "microservice.py"]
