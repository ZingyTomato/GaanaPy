FROM python:alpine

WORKDIR /GaanaPy

COPY api api/
COPY app.py app.py
COPY requirements.txt requirements.txt

EXPOSE 5000

RUN apk add g++ make libffi-dev openssl-dev --no-cache

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]