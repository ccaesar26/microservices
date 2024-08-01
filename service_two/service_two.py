from microskel.service_template import ServiceTemplate
import service_one_proxy_module


class ServiceTwo(ServiceTemplate):

    def get_modules(self):
        return super().get_modules() + [service_one_proxy_module.ServiceTwoModule(self)]

    def get_python_modules(self):
        return super().get_python_modules() + [service_one_proxy_module]

    def custom_function(self, name):  # ca si exemplu
        data = self.injector.get(service_one_proxy_module.ServiceOneProxy).get_hello(name)
        return data


if __name__ == '__main__':
    ServiceTwo().start()