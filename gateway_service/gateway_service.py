from microskel.service_template import ServiceTemplate
import gateway_module


class GatewayService(ServiceTemplate):
    def get_modules(self):
        return super().get_modules() + [gateway_module.GatewayModule(self)]

    def get_python_modules(self):
        return super().get_python_modules() + [gateway_module]


if __name__ == '__main__':
    GatewayService('gateway_service').start()
