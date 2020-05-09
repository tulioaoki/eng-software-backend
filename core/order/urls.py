from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings

from core.carrosel.views import *

urlpatterns = [
    url(r'^carrosel$', CarroselView.as_view()),
    url(r'^carrosel/(?P<pk>[0-9]+)$', CarroselDetail.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)



