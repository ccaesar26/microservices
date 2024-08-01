from injector import Module, Binder, singleton

from microskel.service_discovery import ServiceDiscovery  # interfata
import requests
from decouple import config


class EventProxy:  # TODO: frumos sa fie generate
    def __init__(self, service):
        self.service = service

    def get_events(self, city: str):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('events_service')
        if not endpoint:
            return 'No endpoint', 401
        return requests.get(f'{endpoint.to_base_url()}/events/{city}').json()


class WeatherProxy:  # TODO: frumos sa fie generate
    def __init__(self, service):
        self.service = service

    def get_weather(self, city: str, date: str):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('weather_service')
        if not endpoint:
            return 'No endpoint', 401
        return requests.get(f'{endpoint.to_base_url()}/weather/{city}/{date}').json()


class GatewayModule(Module):
    def __init__(self, gateway_service):
        self.gateway_service = gateway_service

    def configure(self, binder: Binder) -> None:
        event_client = EventProxy(self.gateway_service)
        weather_client = WeatherProxy(self.gateway_service)
        binder.bind(EventProxy, to=event_client, scope=singleton)
        binder.bind(WeatherProxy, to=weather_client, scope=singleton)


def configure_views(app):
    @app.route('/get_events/<city>')
    def get_events(city: str, event_proxy: EventProxy):
        app.logger.info(f'get_events/{city} called in {config("MICROSERVICE_NAME")}')
        data = event_proxy.get_events(city)
        own_data = f'Data for {city} from {config("MICROSERVICE_NAME")}'
        return f'{data} AND {own_data}'

    @app.route('/get_weather/<city>/<date>')
    def get_weather(city: str, date: str, weather_proxy: WeatherProxy):
        app.logger.info(f'get_weather/{city}/{date} called in {config("MICROSERVICE_NAME")}')
        data = weather_proxy.get_weather(city, date)
        own_data = f'Data for {city} from {config("MICROSERVICE_NAME")}'
        return f'{data} AND {own_data}'
