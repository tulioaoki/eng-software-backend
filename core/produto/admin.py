from django.apps import apps, AppConfig
from django.contrib import admin


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ListAdminMixin, self).__init__(model, admin_site)


class CustomApp(AppConfig):
    name = 'core.produto'

    def ready(self):
        models = apps.get_models()
        for model in models:
            admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})

            admin.site.register(model, admin_class)

