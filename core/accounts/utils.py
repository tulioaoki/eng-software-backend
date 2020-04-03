from core.accounts.roles.models import Role
from core.accounts.roles.utils import get_default_role


def serialize_perms_to_front(username):
    list_permissions = []
    return list_permissions


def validate_role(validated_data):
    try:
        if validated_data.get('role') is None:
            return get_default_role()
        role_data = validated_data.get('role')
        role = Role.objects.get(pk=role_data)
        return role
    except:
        return 'role nao cadastrado'


def getUser(user):
    from core.accounts.models import CustomUser
    try:
        user = CustomUser.objects.get(username=user)
        return user
    except CustomUser.DoesNotExist:
        return None