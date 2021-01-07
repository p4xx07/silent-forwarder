import os, inspect
import telepot
from bot_handler import Handler
from telepot import Bot
from telepot.loop import MessageLoop
import bot_handler
import datetime
import time
from config import getConfig

def start(bot: Bot, config):
    handler = Handler(bot)
    MessageLoop(bot, handler.handle).run_as_thread()
    while True:
        #CYCLE EVERY 50 SEC
        #IF 20 min have passed
        #GRAB IMAGE FROM ./img/i.png
        #send to group
        #delete img

config = getConfig()
bot = telepot.Bot(config[0])
start(bot, config)

