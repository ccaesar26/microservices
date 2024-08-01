FROM ccezar26/microskel

ADD . /opt/gateway_service
WORKDIR /opt/gateway_service

RUN pip install -r requirements.txt
CMD ["python", "gateway_service.py"]
