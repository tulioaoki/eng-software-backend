from django.db.models import Q
from core.accounts.models import CustomUser as User


class MyBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        """Autentica o usuario caso a senha confira com o usuario e o mesmo seja ativo."""
        usermodel = User
        try:
            user = usermodel.objects.get(
                Q(username__iexact=username)
            )
            if user.check_password(password) and user.is_active:
                return user
        except usermodel.DoesNotExist:
            pass

