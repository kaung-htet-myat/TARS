import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext
from langchain_core.messages import HumanMessage, SystemMessage

from llm.utils import get_llm_agent
from llm.prompts import get_primer_prompt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
USER_ID = str(os.environ.get('USER_ID', ''))
LLM_URL = os.environ.get('LLM_URL', '')


AGENT_EXECUTOR = get_llm_agent()
SESSION = {
    'user_id': 0,
    'chat_id': 0
}


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I'm TARS. How can I help you?")


async def debug(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    user_id = update.effective_user.id
    
    if str(user_id) == USER_ID:
        await update.message.reply_text(f"Hi Hi my friend")
    else:
        await update.message.reply_text(f"Can't talk to you")
    
    await update.message.reply_text(f"You said and TARS repeat: {user_text}")


async def receive(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.message.chat.id)
    user_id = str(update.effective_user.id)
    user_text = update.message.text
    
    if user_id == USER_ID:
        try:
            config = {
                'configurable': {
                    'thread_id': chat_id,
                    'updater': update,
                    'context': context
                }
            }
            messages = []
            
            if not user_id == SESSION.get('user_id') or not chat_id == SESSION.get('chat_id'):
                SESSION['user_id'] = user_id
                SESSION['chat_id'] = chat_id
                
                primer_prompt = get_primer_prompt()
                messages.append(SystemMessage(content=primer_prompt))

            messages.append(HumanMessage(content=user_text))

            response = AGENT_EXECUTOR.invoke(
                {"messages": messages},
                config=config,
            )
            
            for message in response['messages']:
                logger.info(message)

            reply = response['messages'][-1].content
            await update.message.reply_text(reply)
            
        except Exception as e:
            logger.error(e)
            await update.message.reply_text(f"I cannot reply to you right now.")