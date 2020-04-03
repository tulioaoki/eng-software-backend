from core.accounts.roles.models import Role


def get_default_role():
    #returns default role
    r,created = Role.objects.get_or_create(role='1')
    return r