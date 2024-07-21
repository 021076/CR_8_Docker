from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


class Action(models.Model):
    """ Модель 'Действие', типы: useful-полезное, pleasant-приятное, award-вознаграждение"""
    TYPE_ACTION = (('useful', 'useful'), ('pleasant', 'pleasant'), ('award', 'award'))
    objects = None
    title = models.CharField(max_length=200, verbose_name='Название действия')
    type_action = models.CharField(max_length=20, choices=TYPE_ACTION, verbose_name='Тип действия')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'


class Habit(models.Model):
    """ Модель 'Привычка'"""
    objects = None
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='action', verbose_name='Действие')
    is_pleasant = models.BooleanField(verbose_name='Приятная привычка', **NULLABLE)
    link_action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='link_action',
                                    verbose_name='Связанная привычка', **NULLABLE)
    award = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='award', verbose_name='Вознаграждение',
                              **NULLABLE)
    space = models.CharField(max_length=150, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    periodicity = models.PositiveIntegerField(verbose_name='Периодичность выполнения',
                                              help_text='Количество выполнений - количество дней в неделю (например: 1 - один раз в неделю, 7 - каждый день)')
    runtime = models.DurationField(verbose_name='Время на выполнение')
    is_public = models.BooleanField(verbose_name='Публичность')
    last_date = models.DateTimeField(verbose_name='Дата последнего выполнения', **NULLABLE)

    def __str__(self):
        return {self.action}

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
