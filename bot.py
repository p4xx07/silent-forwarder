import os
import handler
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

token = os.environ["TOKEN"]
channel_id = os.environ["CHANNEL_ID"]
valid_users = os.environ["VALID_USERS"].split(",")

updater = Updater(token=token)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

handler.set_valid_users(valid_users)

start_handler = CommandHandler("start", handler.start)
restart_handler = CommandHandler("stop", handler.stop)
stop_handler = CommandHandler("restart", handler.restart)
media_handler = MessageHandler(
    (
        Filters.animation
        | Filters.video
        | Filters.photo
    )
    & Filters.chat_type.private,
    handler.save_media,
)
unknown_handler = MessageHandler(
    Filters.command & Filters.chat_type.private, handler.unknown
)

dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(restart_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(media_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

handler.restarted(updater.bot)
handler.reminder(updater.bot, channel_id)

updater.idle()
