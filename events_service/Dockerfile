FROM ccezar26/microskel

ADD . /opt/events_service
WORKDIR /opt/events_service

RUN pip install -r requirements.txt

CMD ["python", "events_service.py"]
