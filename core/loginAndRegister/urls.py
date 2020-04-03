from rest_framework.urlpatterns import format_suffix_patterns
from core.loginAndRegister import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^check-auth$', views.CheckAuth.as_view()),
    url(r'^forgot-password$', views.ForgotPassword.as_view()),
    url(r'^change-password$', views.ChangePassword.as_view()),
    url(r'^login$', views.CustomLogin.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)

