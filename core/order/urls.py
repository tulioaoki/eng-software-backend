from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings

from core.carrosel.views import *
from core.order.views import OrderView, OrderDetail

urlpatterns = [
    url(r'^order', OrderView.as_view()),
    url(r'^order/(?P<pk>[0-9]+)$', OrderDetail.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)



