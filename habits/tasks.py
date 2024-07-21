import datetime
from celery import shared_task
from habits.models import Habit
from habits.services import telegram_sending


@shared_task
def send_notify_habit_tg():
    time_now = datetime.datetime.now().time()
    date_now = datetime.datetime.now()
    habits = Habit.objects.all()
    for habit in habits:
        if habit.last_date == date_now - datetime.timedelta(days=habit.periodicity) and habit.time >= time_now:
            if habit.user.tg_chat_id:
                chat_id = habit.user.tg_chat_id
                if not habit.is_pleasant and not habit.link_action:
                    message = f'вам нужно выполнить'
                    # # if not habit.is_pleasant and habit.link_action:
                    # #     message = 'вам нужно выполнить полезное действие вместе с приятным'
                    # elif not habit.is_pleasant and habit.award:
                    #     message = f'вам нужно выполнить полезное и получить вознаграждение'
                    # elif habit.is_pleasant:
                    #     message = f'вам нужно выполнить приятная привычка'
                    telegram_sending(chat_id, message)
        habit.last_date = date_now
        habit.save()
