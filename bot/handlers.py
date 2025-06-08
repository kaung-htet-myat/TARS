import base64
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes

from llm.utils import get_llm_agent
from llm.prompts import get_primer_prompt
from config.config import get_settings
from llm.conversations import ConversationState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


settings = get_settings()
TIMEZONES = ["Asia/Bangkok", "Asia/Singapore"]


if not settings.user_ids:
    logger.error("No users registered.")
else:
    settings.user_ids = settings.user_ids.split(",")
    settings.user_timezone = dict(
        zip(settings.user_ids, ["Asia/Bangkok"] * len(settings.user_ids))
    )


AGENT_EXECUTOR = get_llm_agent(openai_api_key=settings.openai_api_key)


async def start(update: Update, context: CallbackContext) -> None:
    logger.info(f"New user detected: {update.effective_user.id}")
    keyboard = [[InlineKeyboardButton(tz, callback_data=tz)] for tz in TIMEZONES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if str(update.effective_user.id) in settings.user_ids:
        await update.message.reply_text(
            "Hello! I'm TARS. How can I help you?\nPlease select your timezone:",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text("Can't talk to you right now")


async def timezone_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_timezone = query.data
    user_id = str(update.effective_user.id)
    if user_id in settings.user_ids:
        settings.user_timezone.update({user_id: selected_timezone})
        await query.edit_message_text(f"Timezone set to: {selected_timezone}")

        primer_prompt = get_primer_prompt()
        primer_prompt = primer_prompt.format(timezone=selected_timezone)
        conversation = ConversationState(primer_prompt)
        settings.sessions.update({user_id: conversation})
    else:
        await query.edit_message_text("Can't talk to you right now")


async def receive(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.message.chat.id)
    user_id = str(update.effective_user.id)
    user_text = update.message.text
    user_photo = update.message.photo
    user_attachment = update.message.effective_attachment

    if user_id in settings.user_ids:
        try:
            config = {
                "configurable": {
                    "thread_id": chat_id,
                    "updater": update,
                    "context": context,
                    "timezone": settings.user_timezone.get(user_id),
                }
            }

            conversation = settings.sessions.get(user_id)

            if user_text is not None:
                conversation.add_user_message(user_text)

            if not len(user_photo) == 0:
                photo = user_photo[-1]  # Get the highest quality image
                file = await context.bot.get_file(photo.file_id)
                ba = await file.download_as_bytearray()

                image_data = base64.b64encode(ba).decode("utf-8")
                content = [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ]
                conversation.add_user_message(content)

            if user_attachment is not None and "image" in user_attachment.mime_type:
                file = await context.bot.get_file(user_attachment.file_id)
                ba = await file.download_as_bytearray()

                image_data = base64.b64encode(ba).decode("utf-8")
                content = [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ]
                conversation.add_user_message(content)

            response = AGENT_EXECUTOR.invoke(
                conversation.get_state(),
                config=config,
            )

            reply = response["messages"][-1].content
            await update.message.reply_text(reply)

        except Exception as e:
            logger.error(e)
            await update.message.reply_text("I cannot reply to you right now.")
