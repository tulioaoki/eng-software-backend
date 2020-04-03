from django.core.mail import send_mail
from django.http import Http404

from core.accounts.models import CustomUser


def forgot_password_email(email,password):
    """Envia email de recuperacao de senha"""
    body = "Recuperacao de senha\n" \
           "Senha temporaria : {}".format(password)
    send_mail(
        'Recuperacao de senha',
        body,
        from_email="ijud@arkiv.com.br",
        recipient_list=[email,],
        fail_silently=False,
    )


def get_role(request):
    """Retorna role do usuario"""
    try:
        username = request.data.get('username')
        user = CustomUser.objects.get(username=username)
        user_role = user.role.getRole()
        return user_role
    except CustomUser.DoesNotExist:
        raise Http404