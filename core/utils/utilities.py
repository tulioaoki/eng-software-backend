from ast import literal_eval

from django.contrib.auth.decorators import user_passes_test
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.exceptions import PermissionDenied, FieldError
from django.db.models.query import QuerySet
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from core.produto.models import Product

filterable_foreign_keys = (

)

def paginated_response_dict(objects, request):
    if request and (objects or type(objects) == QuerySet):
        if(len(objects) == 0):
            return {'objects': [], 'page': 1, "item_count": 0}
        get_data = request.query_params  # or request.GET check both
        data = get_data
        data._mutable = True
        from django.core.paginator import Paginator
        page = 1
        page_size = 10
        item_count = len(objects)
        if 'page' in data.keys():
            page = int(data.pop('page', [1])[0])
            if page and page < 1:
                page = 1
        if 'page_size' in data.keys():
            page_size = int(data.pop('page_size',[10])[0])
        p = Paginator(objects, page_size)
        if page > p.page_range[-1]:
            raise ObjectNotFound("Page index out of range, max index is: {}".format(p.page_range[-1]))
        return {'objects': p.page(page).object_list, 'page': page, "item_count": item_count}


def default_response(code, message, success, data=None,status_code=None ,pagination_data=None):
    """
    Gera uma resposta padronizada baseada no sucesso da requisicao HTTP
    Caso haja sucesso, retorna o status_code padrao de sucesso, um codigo, sucesso, uma mensagem e objeto (caso haja)
    Caso haja falha, retorna objeto de erro e mensagem de erro.
    """
    if pagination_data is None:
        pagination_data = {}
    objects = pagination_data.get('objects')
    page = pagination_data.get('page') if pagination_data.get('page') else 1
    page_size = len(objects) if objects else (len(data) if type(data) == 'list' else 1)
    item_count = pagination_data.get('item_count') if pagination_data.get('item_count') is not None else (len(data) if type(data) == 'list' else 1)
    if success:
        return{
                'code':code,
                'success':True,
                'message': message,
                'data': (data if data is not None else []),
                'page':page,
                'page_size':page_size,
                'item_count':item_count
              }
    else:
        return {
                'code':code,
                'success': False,
                'message': message,
                'errors': (data if data is not None else []),
                'page': None,
                'page_size': None,
                'item_count': None
              }


def permission_required(raise_exception=True,*perms,**kwargs):
    """
    Funcao de verificacao de permissao que adiciona verificacao de permissoes customizadas.
    """

    def check_perms(user):
        if kwargs:
            modulo = kwargs.get('modulo')
            perm = kwargs.get('perm')
        else:
            modulo=None
            perm=None
        for p in perm:
            if user.has_customPerm(modulo=modulo, perm=p):
                return True
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms,lambda u: any(u.has_perm(perm) for perm in perms))


def custom_permission_required(modulo, perms,raise_exception=True):
    """
    Esta funcao verifica se o usuario possui permissoes especificas a partir de variaveis booleanas encontradas
    dentro de cada modulo e permissoes.

    Esta funcao permite que a manutencao de permissoes seja mutavel a partir do banco de dados.
    """

    def check_perms(user):
        if user.is_active and (user.is_admin or user.is_superuser):
            return True
        for p in perms:
            if user.has_customPerm(modulo=modulo, perm=p):
                return True
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms,lambda u: any(u.has_perm(perm) for perm in perms))


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


def custom_filter(objects, request, type=None):

    try:
        """ 
        Este filtro utiliza as informacoes vindas da URL.
        Caso existam chaves especiais na requicao da URL, sao retiradas para que nao interfiram no filtro do QuerySet.
        As chaves restantes (chaves do model) serao utilizadas para filtrar o queryset.
        """
        get_data = request.query_params  # or request.GET check both
        kwargs = {}
        data = get_data
        data._mutable = True
        ordering = False
        limit = False
        categories=[]
        if 'categories' in data.keys():
            categories = data.pop('categories')
        if categories:
            objects = objects.filter(categories__in=literal_eval(categories[0])).distinct()
        if 'limit' in data.keys():
            limit = data.pop('limit')
        if 'order' in data.keys():
            ordering = data.pop('order')[0]
        if 'search' in data.keys():
            """
            A key 'Search' é utilizada para procurar alguma string dentro de campos de string/texto no objeto.
            """
            searched = data.get('search')
            query = SearchQuery(searched)
            vector = SearchVector('name', 'description')
            objects = objects.annotate(search=vector).filter(search=query)
        """
        Filtra a queryset com as keys presentes na URL
        """
        for keys in data.keys():
                kwargs[str(keys)] = str(get_data[keys])
                kwargs.pop('page', None)
                kwargs.pop('categories', None)
                kwargs.pop('page_size', None)
                objects = objects.filter(**kwargs)

        if ordering:
            """
            Ordena a query de acordo com o campo solicitado na URL
            """
            objects = objects.order_by(ordering)
        if limit:
            """
            Caso o campo 'limit' esteja presente na URL,
             limita o numero de objetos a serem retornados de acordo com o solicitado
            """
            objects = objects.all()[:int(limit)]
        return objects
    except FieldError:
        return objects
    except ValueError:
        raise ObjectNotFound('Invalid search field')


class ObjectNotFound(APIException):
    status_code = 404
    default_detail = 'Object not found.'
    default_code = 'object_not_found'


import re

from django.contrib.postgres.search import SearchQuery


class RawSearchQuery(SearchQuery):
    """Override to use to_tsquery instead of plainto_tsquery

    Allows formatted search terms for things like prefix matching search.

    This feature is coming in django 2.2 in april 2019 so remove and use that when
    possible.
    """
    def as_sql(self, compiler, connection):
        params = [self.value]
        if self.config:
            config_sql, config_params = compiler.compile(self.config)
            template = 'to_tsquery({}::regconfig, %s)'.format(config_sql)
            params = config_params + [self.value]
        else:
            template = 'to_tsquery(%s)'
        if self.invert:
            template = '!!({})'.format(template)
        return template, params


def prepare_search_term(term: str) -> str:
    """Sanitize the input term for a search using postgres to_tsquery.

    Cleans a search string to something acceptable for use with to_tsquery.
    Appends ':*' so that partial matches will also be returned.

    Args:
        term: the search term to be cleaned and prepared

    Returns:
        the prepared search string
    """

    query = re.sub(r'[!\'()|&]', ' ', term).strip()
    if query:
        query = re.sub(r'\s+', ' & ', query)
        query += ':*'

    return query