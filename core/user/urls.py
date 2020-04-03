from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from core.user.views import GoogleView, HelloView

urlpatterns = [
    url(r'^google$', GoogleView.as_view()),
    url(r'^hello$', HelloView.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)



