from typing import Dict, Any

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'myapp'
    container: Dict[str, Any]

    def ready(self) -> None:
        from myapp.hexagonal_configuration import build_production_ioc_container
        self.container = build_production_ioc_container()

