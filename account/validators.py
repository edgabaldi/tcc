#coding:utf-8
import re
import datetime

from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES

def validate_birth_date(birth_date):
    today = datetime.date.today()
    year = today.year - 18
    limit_date = today.replace(year=year)
    if birth_date > limit_date:
        raise ValidationError("Invalid Birth Date")

def validate_cpf_cnpj(value):

    validator = CPFCNPJValidation(value)

    try:
        validator.validate_cpf()
    except ValidationError:
        validator.validate_cnpj()


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0

class CPFCNPJValidation(object):

    error_messages = {
        'invalid': "Invalid CPF or CNPJ number.",
        'digits_only': "This field requires only numbers.",
        'max_digits': "This field requires at most 11 digits for CPF or 14 digits for CNPJ.",
    }

    def __init__(self, value):
        self.value = value

    def validate_cpf(self):
        """
        Value can be either a string in the format XXX.XXX.XXX-XX or an
        11-digit number.
        """

        if self.value in EMPTY_VALUES:
            return u''
        if not self.value.isdigit():
            self.value = re.sub("[-\.]", "", self.value)
        orig_value = self.value[:]
        try:
            int(self.value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])
        if len(self.value) != 11:
            raise ValidationError(self.error_messages['max_digits'])
        orig_dv = self.value[-2:]

        new_1dv = sum([i * int(self.value[idx]) for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        self.value = self.value[:-2] + str(new_1dv) + self.value[-1]
        new_2dv = sum([i * int(self.value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        self.value = self.value[:-1] + str(new_2dv)
        if self.value[-2:] != orig_dv:
            raise ValidationError(self.error_messages['invalid'])
        return orig_value

    def validate_cnpj(self):
        ## Try to Validate CNPJ
        """
        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
        group of 14 characters.
        """
        if self.value in EMPTY_VALUES:
            return u''
        if not self.value.isdigit():
            self.value = re.sub("[-/\.]", "", self.value)
        orig_value = self.value[:]
        try:
            int(self.value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])
        if len(self.value) != 14:
            raise ValidationError(self.error_messages['max_digits'])
        orig_dv = self.value[-2:]

        new_1dv = sum([i * int(self.value[idx]) for idx, i in enumerate(range(5, 1, -1) + range(9, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        self.value = self.value[:-2] + str(new_1dv) + self.value[-1]
        new_2dv = sum([i * int(self.value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        self.value = self.value[:-1] + str(new_2dv)
        if self.value[-2:] != orig_dv:
            raise ValidationError(self.error_messages['invalid'])

        return orig_value
