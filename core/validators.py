import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

error_messages = {
    'invalid': ("Invalid CPF/CNPJ number."),
    'digits_only': ("This field requires only numbers."),
    'max_digits': ("This field requires exactly 11 digits."),
}


def validate_email_username(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False


def only_numbers(value):
    if not value.isdigit():
        raise ValidationError('Only numbers.', 'digits')


def five_digits(value):
    if len(str(value)) > 5:
        return 0


def validate_12_digits(value):
    if len(value) != 12:
        raise ValidationError('O numero de solicitacao possui 12 digitos.')


def validate_20_digits(value):
    if len(value) != 20:
        raise ValidationError('O numero deve possuir 20 digitos.')


def processo_validator(value):  # Verifica se o processo possui apenas numeros e tamanho certo
    if not value.isdigit():
        raise ValidationError('Only numbers.', 'digits')
    if len(value) < 20:
        raise ValidationError('Deve ter 20 numeros', 'tamanho')


def validate_cpf_cnpj(value):
    if len(value) == 11:
        digito = {}
        digito[0] = 0
        digito[1] = 0
        a = 10
        total = 0
        for c in range(0, 2):
            for i in range(0, (8 + c + 1)):
                total = total + int(value[i]) * a
                a = a - 1
            digito[c] = int(11 - (total % 11))
            a = 11
            total = 0
        if not (int(value[9]) == int(digito[0]) and int(value[10]) == int(digito[1])):
            raise ValidationError('CPF/CNPJ invalido')
    elif len(value) == 14:
        def DV_maker(v):
            if v >= 2:
                return 11 - v
            return 0

        """
            Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
            group of 14 characters.
            :type value: object
            """
        value = str(value)
        if not value.isdigit():
            value = re.sub("[-/\.]", "", value)
        try:
            int(value)
        except ValueError:
            raise ValidationError(error_messages['digits_only'])
        if len(value) > 14:
            raise ValidationError(error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(5, 1, -1)) + list(range(9, 1, -1)))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(6, 1, -1)) + list(range(9, 1, -1)))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise ValidationError(error_messages['invalid'])
    else:
        raise ValidationError('Enter a valid CPF-CNPJ.')


def validate_value(value):
    if not value.isdigit() or int(value) < 0:
        raise ValidationError('Must contain a valid value.', 'digits')


def validate_phone(value):
    if not value.isdigit():
        raise ValidationError('Phone should be only numbers.', 'digits')

    if len(value) < 9:
        raise ValidationError('Invalid phone number.', 'number with less than 9 digits')


def only_char(value):
    if not all(x.isalpha() or x.isspace() for x in value):
        raise ValidationError('Should contain only char.', 'Only char')


def positive(value):
    if int(value) < 0:
        raise ValidationError('Should contain only positive numbers.', 'digits')


def ref_validator(value):
    if value > 9999 or value == 0:
        raise ValidationError('Ref should not have more than four digits and cannot be zero.', '4 digits or zero')


def partials_validator(value):
    if value > 100 or value < 1:
        raise ValidationError('Partials must be between 1 and 100.')


def not_zero(value):
    if value == 0:
        raise ValidationError('Cannot be zero.', 'number is zero')


def address(value):
    if '!' in value or '?' in value:
        raise ValidationError("Should not contain '?' or '!'.", 'Only char')
