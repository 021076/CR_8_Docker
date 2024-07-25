from django.urls import path
from rest_framework.routers import DefaultRouter
from habits.apps import HabitsConfig
from habits.views import ActionViewSet, HabitListAPIView, HabitCreateAPIView, PublicHabitListAPIView, \
    HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'action', ActionViewSet, 'action')

urlpatterns = [
                  path('list/', HabitListAPIView.as_view(), name='habit_list'),
                  path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
                  path('public_list/', PublicHabitListAPIView.as_view(), name='habit_public_list'),
                  path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_retrieve'),
                  path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
                  path('habit/destroy/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_destroy'),
              ] + router.urls
