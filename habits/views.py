import pytz
from datetime import datetime, timedelta
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from config import settings
from habits.models import Action, Habit
from habits.paginators import HabitPagination
from habits.serializers import ActionSerializer, HabitSerializer
from users.permissions import IsOwner, ListIsPublicHabits


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    def perform_create(self, serializer):
        """Переопределение метода create, владельцем становится авторизованный пользователь создающий действие"""
        new_action = serializer.save()
        new_action.user = self.request.user
        new_action.save()

    def get_permissions(self):
        """ Разрешения:
        создание действия - любому авторизованному пользователю,
        просмотр списка и детализации действия - любому авторизованному пользователю,
                                                для неавторизованных пользователей только чтение
        обновление и удаление действия - только Пользователю"""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ]
        elif self.action in ('retrieve', 'list'):
            self.permission_classes = [IsAuthenticatedOrReadOnly | IsOwner, ]
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = [IsOwner, ]
        return super().get_permissions()


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки, метод create"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        """Переопределение метода create:
        владельцем становится авторизованный пользователь создающий действие
        дата следующего напоминания = текущая + Периодичность выполнения
        если создается привычка на приятное действие, чек-бокс is_pleasant = True
        """
        timezone = pytz.timezone(settings.TIME_ZONE)
        date_now = datetime.now(timezone)
        new_habit = serializer.save()
        new_habit.next_date = date_now + timedelta(days=new_habit.periodicity)
        new_habit.user = self.request.user
        if new_habit.action in Action.objects.filter(type_action='pleasant'):
            new_habit.is_pleasant = True
        new_habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Обновление привычки, метод put, patch"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner, ]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки, метод delete"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner, ]


class HabitListAPIView(generics.ListAPIView):
    """Вывод списка привычек пользователя метод get"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsOwner, ]

    def get_queryset(self):
        """Параметры вывода списка привычек"""
        queryset = Habit.objects.filter(user=self.request.user)
        return queryset


class PublicHabitListAPIView(generics.ListAPIView):
    """Вывод списка публичных привычек метод get"""
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [ListIsPublicHabits, ]

    def get_queryset(self):
        """Параметры вывода списка публичных привычек"""
        queryset = Habit.objects.filter(is_public=True)
        return queryset


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Вывод детализации привычки метод get"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner, ]
