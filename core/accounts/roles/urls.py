from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from core.accounts.roles import views

urlpatterns = [
    url(r'^roles$', views.ViewAllRoles.as_view()),
    url(r'^criar-roles$', views.RolesPost.as_view()),
    url(r'^roles/(?P<pk>[0-9]+)$', views.RoleDetail.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)

