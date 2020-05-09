from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('core.produto.urls')),
    url(r'^', include('core.purchases.urls')),
    url(r'^', include('core.categoria.urls')),
    url(r'^', include('core.carrosel.urls')),
    url(r'^', include('core.user.urls')),
    url(r'^', include('core.accounts.urls')),
    url(r'^', include('core.loginAndRegister.urls')),

    #admin
    url(r'^admin/', admin.site.urls),
]