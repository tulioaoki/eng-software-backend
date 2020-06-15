from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from core.produto.views import Produtos, ProdutoDetail, ProductImageView, ProductImageDetail, OfferDetail, \
    OfferView, ProdutosRecentes, ProdutosBestSellers

urlpatterns = [
    url(r'^products$', Produtos.as_view()),
    url(r'^products/best_sellers$', ProdutosBestSellers.as_view()),
    url(r'^products/recent$', ProdutosRecentes.as_view()),
    url(r'^products/(?P<pk>[0-9]+)$', ProdutoDetail.as_view()),
    url(r'^products-images$', ProductImageView.as_view()),
    url(r'^products-images/(?P<pk>[0-9]+)$', ProductImageDetail.as_view()),
    url(r'^offers$', OfferView.as_view()),
    url(r'^offers/(?P<pk>[0-9]+)$', OfferDetail.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)



