from rest_framework import serializers
from habits.models import Action, Habit
from habits.validators import MutuallyExclusiveFieldsValidator, PeriodicityValidator, RunTimeValidator


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [MutuallyExclusiveFieldsValidator(), RunTimeValidator(), PeriodicityValidator()]
