FROM alpine:latest

EXPOSE 5000

RUN apk add git py3-pip gcc g++ make libffi-dev openssl-dev --no-cache

RUN git clone https://github.com/ZingyTomato/GaanaPy

RUN cd GaanaPy && pip3 install -r requirements.txt

CMD ["python3", "GaanaPy/app.py"]
