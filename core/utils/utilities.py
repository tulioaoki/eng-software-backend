from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied, FieldError
from django.db.models import CharField, TextField, Func, Q
from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

filterable_foreign_keys = (

)


def default_response(code,message,success,data=None,status_code=None):
    """
    Gera uma resposta padronizada baseada no sucesso da requisicao HTTP
    Caso haja sucesso, retorna o status_code padrao de sucesso, um codigo, sucesso, uma mensagem e objeto (caso haja)
    Caso haja falha, retorna objeto de erro e mensagem de erro.
    """
    if success:
        return{
                'code':code,
                'success':True,
                'message': message,
                'data': (data if data is not None else []),
              }
    else:
        return {
                'code':code,
                'success': False,
                'message': message,
                'errors': (data if data is not None else []),
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


def custom_filter(objects, request):

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
        if 'limit' in data.keys():
            limit = data.pop('limit')
        if 'ordering' in data.keys():
            ordering = data.pop('ordering')[0]
        if 'search' in data.keys():
            """
            A key 'Search' é utilizada para procurar alguma string dentro de campos de string/texto no objeto.
            """
            searched = data.get('search')
            objects = objects.filter(pk__icontains=searched)
            return objects
        """
        Filtra a queryset com as keys presentes na URL
        """
        for keys in data.keys():
                kwargs[str(keys)] = str(get_data[keys])
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


def custom_filter_processo(objects, request):

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
        if 'limit' in data.keys():
            limit = data.pop('limit')
        if 'ordering' in data.keys():
            ordering = data.pop('ordering')[0]
        if 'search' in data.keys():
            """
            A key 'Search' é utilizada para procurar alguma string dentro de campos de string/texto no objeto.
            """
            searched = data.get('search')

            objects = objects.filter(
                        Q(numero_processo__icontains=searched) |
                        Q(autor__autor__icontains=searched) |
                        Q(complemento_status__icontains=searched) |
                        Q(observacoes__icontains=searched) |
                        Q(descricao__icontains=searched) |
                        Q(classificacao__classificacao__icontains=searched) |
                        Q(classificacao__label__icontains=searched)

            )
            return objects
        """
        Filtra a queryset com as keys presentes na URL
        """
        for keys in data.keys():
                kwargs[str(keys)] = str(get_data[keys])
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