import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from bot.handlers import start, receive, timezone_selection
from config.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


settings = get_settings()


def main():
    app = Application.builder().token(settings.bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(timezone_selection))
    app.add_handler(
        MessageHandler(
            (filters.TEXT | filters.PHOTO | filters.ATTACHMENT) & ~filters.COMMAND,
            receive,
        )
    )

    logger.info("TARS is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
