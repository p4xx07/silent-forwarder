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
        time.sleep(30)
        continue
        if handler.active is False:
            time.sleep(60)
            return
        if(time.time() - last_epoch >= 60 * 0):
            handler.sendImageToChannel()
            last_epoch = time.time()
        time.sleep(60)

config = getConfig()
bot = telepot.Bot(config[0])
start(bot, config)

