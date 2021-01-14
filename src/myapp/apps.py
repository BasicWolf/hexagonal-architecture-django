from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'myapp'
    container: dict

    def ready(self):
        from myapp.hexagonal_configuration import build_production_ioc_container
        self.container = build_production_ioc_container()

