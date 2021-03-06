from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings

from core.categoria.views import Categorias, CategoriaDetail
from core.produto.views import Produtos, ProdutoDetail

urlpatterns = [
    url(r'^categories$', Categorias.as_view()),
    url(r'^categories/(?P<pk>[0-9]+)$', CategoriaDetail.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)



