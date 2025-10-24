from django.apps import AppConfig


class CarteiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carteira'

    def ready(self):
        import carteira.signals