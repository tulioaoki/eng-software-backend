from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings

from core.purchases import views

urlpatterns = [
    url(r'^cart$', views.CartView.as_view()),
    url(r'^cart/(?P<pk>[0-9]+)$', views.CartEdit.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)



