from telegram.ext import CallbackContext


async def send_message_callback(context: CallbackContext):
    """Callback function executed by the job queue"""
    
    job_data = context.job.data
    await context.bot.send_message(chat_id=job_data['chat_id'], text=job_data['message'])