from microskel.service_template import ServiceTemplate
import weather_module


class WeatherService(ServiceTemplate):
    def __init__(self, name):
        super().__init__(name)

    def get_python_modules(self):
        return super().get_python_modules() + [weather_module]


if __name__ == '__main__':
    WeatherService('weather_service').start()
