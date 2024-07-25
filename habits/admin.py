from django.contrib import admin
from habits.models import Action, Habit


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type_action', 'user',)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'action',)
