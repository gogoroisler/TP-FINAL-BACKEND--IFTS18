from django.apps import AppConfig


class ExpensasConfig(AppConfig):
    name = 'expensas'

    def ready(self):
        import expensas.signals  # noqa: F401
