import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.handlers import start, debug, receive


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
TOKEN = os.environ.get('BOT_TOKEN', '')


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.ATTACHMENT) & ~filters.COMMAND, receive))

    logger.info("TARS is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
