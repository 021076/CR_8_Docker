import datetime
from rest_framework.serializers import ValidationError
from habits.models import Action


class MutuallyExclusiveFieldsValidator:
    """Валидатор взаимоисключающих полей"""

    def __call__(self, value, null=None):
        check_field1 = dict(value).get('link_action')
        # print(check_field1)
        check_field2 = dict(value).get('award')
        # print(check_field2)
        check_field3 = dict(value).get('is_pleasant')
        # print(check_field3)
        actions = Action.objects.all()
        for obj in actions:
            if obj.type_action != 'pleasant' and str(obj.title) == str(check_field1):
                # print(f'{check_field1}:{obj.title}')
                raise ValidationError(
                    f'В связанные привычки могут попадать только привычки с признаком приятной привычки')
        if check_field1 is not null and check_field2 is not null:
            raise ValidationError(
                f'Одновременный выбор связанной привычки и указания вознаграждения запрещены')
        elif check_field3 and (check_field1 is not null or check_field2 is not null):
            raise ValidationError(
                f'У приятной привычки не может быть вознаграждения или связанной привычки')


class RunTimeValidator:
    """Валидатор на время выполнения"""

    def __call__(self, value, null=None):
        check_field = dict(value).get('runtime')
        max_runtime = datetime.timedelta(seconds=120)
        if check_field and check_field > max_runtime:
            print(type(check_field), type(max_runtime))
            raise ValidationError(
                f'Время выполнения должно быть не больше 120 секунд')


class PeriodicityValidator:
    """Валидатор на промежуток между выполнениями"""

    def __call__(self, value, null=None):
        check_field = dict(value).get('periodicity')
        # print(type(check_field))
        if check_field and int(check_field) > 7:
            raise ValidationError(
                f'Нельзя выполнять привычку реже, чем 1 раз в 7 дней')
