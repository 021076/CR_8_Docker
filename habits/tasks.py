from datetime import datetime, timedelta
import pytz
from celery import shared_task
from config import settings
from habits.models import Habit
from habits.services import telegram_sending


@shared_task
def send_notify_habit_tg():
    timezone = pytz.timezone(settings.TIME_ZONE)
    date_now = datetime.now(timezone)
    habits = Habit.objects.all()
    for habit in habits:
        if habit.user.tg_chat_id and date_now.date() == habit.next_date.date() and date_now.time() >= habit.time:
            chat_id = habit.user.tg_chat_id
            message = f'Вам нужно {habit.action} в {habit.time}, место - {habit.space}'
            telegram_sending(chat_id, message)
            habit.next_date += timedelta(days=habit.periodicity)
            habit.save()
