from microskel.service_template import ServiceTemplate
import event_module


class EventsService(ServiceTemplate):
    def __init__(self, name):
        super().__init__(name)

    def get_python_modules(self):
        return super().get_python_modules() + [event_module]


if __name__ == '__main__':
    EventsService('events_service').start()
