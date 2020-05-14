from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from core.accounts import views

urlpatterns = [
    url(r'^register$', views.UserCreate.as_view(), name='register'),
    url(r'^users$', views.ViewAllUsers.as_view()),
    url(r'^users/(?P<pk>[0-9]+)$', views.UsersGet.as_view()),
    url(r'^favorites$', views.FavoritesView.as_view()),
    url(r'^favorites/(?P<pk>[0-9]+)$', views.FavoritesDelete.as_view()),
    url(r'^my-profile$', views.MyProfile.as_view()),
    url(r'^users/inactivate$', views.InactivateUser.as_view()),
    url(r'^users/activate$', views.ActivateUser.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)

