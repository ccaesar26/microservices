from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.exc import *

from microskel.db_module import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    city = Column(String(128))
    date = Column(Date)
    name = Column(String(256))
    description = Column(Text)

    def __init__(self, city, date, name, description):
        self.city = city
        self.date = date
        self.name = name
        self.description = description

    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if '_state' not in k:
                if k == 'date' and self.__dict__[k] is not None:
                    d[k] = self.__dict__[k].isoformat()  # Convert date to string
                else:
                    d[k] = self.__dict__[k]
        return d


def configure_views(app):
    @app.route('/events', methods=['POST'])
    def create(request: Request, db: SQLAlchemy):
        event = Event(
            city=request.form.get('city'),
            date=request.form.get('date'),
            name=request.form.get('name'),
            description=request.form.get('description'))
        db.session.add(event)
        db.session.commit()
        return 'OK', 201

    @app.route('/events/<city>', methods=['GET'])
    def get_events(city: str, db: SQLAlchemy):
        try:
            event = db.session.query(Event).filter(Event.city == city).first()
        except NoResultFound as e:
            response = jsonify(status='No event found', context=city)
            response.status = '404'
            return response
        else:
            if not event:
                return jsonify(status='No event found', context=city), 404
            return event.to_dict(), 200
