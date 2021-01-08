import os
import telepot
from bot_handler import Handler
from telepot import Bot
from telepot.loop import MessageLoop
import bot_handler
import time
from config import getConfig

def start(bot: Bot, config):
    handler = Handler(bot)
    MessageLoop(bot, handler.handle).run_as_thread()
    last_epoch = time.time()
    while True:
        if handler.active is False:
            time.sleep(60)
            return
        if(time.time() - last_epoch >= 60 * 20):
            handler.sendImageToChannel()
            last_epoch = time.time()
        time.sleep(60)

config = getConfig()
bot = telepot.Bot(config[0])
start(bot, config)

