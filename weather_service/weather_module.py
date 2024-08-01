from flask import *
import redis
import os

client = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis-weather'), port=6379, db=0, decode_responses=True)


def configure_views(app):
    @app.route('/weather', methods=['POST'])
    def create(request: Request):
        keys = ['temperature', 'humidity', 'wind']
        weather = {k: request.form.get(k) for k in keys}
        city = request.form.get('city', 'unknown')
        date = request.form.get('date', '')
        key = f'{city}:{date}' if date else city

        client.set(key, json.dumps(weather))

        return 'OK', 201

    @app.route('/weather/<city>/<date>', methods=['GET'])
    def get_weather(city: str, date: str):
        key = f'{city}:{date}'
        weather = client.get(key)
        if not weather:
            return jsonify(status='No weather found', context=key), 404
        return jsonify(json.loads(weather)), 200
