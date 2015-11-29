import datetime

from django.core.exceptions import ValidationError

def validate_birth_date(birth_date):
    limit_date = datetime.date.today() - datetime.timedelta(18)
    if birth_date > limit_date:
        raise ValidationError("Invalid Birth Date")
