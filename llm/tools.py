import datetime
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from bot.callbacks import send_message_callback


@tool
def get_current_datetime() -> str:
   """
   Function that returns current date and time in python datetime.datetime format
   """
   return datetime.datetime.now().isoformat()


@tool
def telegram_reminder_call(iso_schedule_time: str, message: str, config: RunnableConfig) -> str:
   """
   Function to send a reminder to a telegram bot
   Args:
    iso_schedule_time: scheduled time in iso format to set a reminder to the telegram bot
    message: reminder message to send to telegram bot at scheduled time
   """
   
   if config:
      updater = config['configurable']['updater']
      context = config['configurable']['context']

   chat_id = updater.effective_chat.id
   
   schedule_time = datetime.datetime.fromisoformat(iso_schedule_time)
   # schedule_time = pytz.timezone(TIMEZONE).localize(schedule_time)

   # Add a job to JobQueue, passing data as a dictionary
   context.job_queue.run_once(send_message_callback, schedule_time, data={'chat_id': chat_id, 'message': message})
   
   return "Reminder set successfully"