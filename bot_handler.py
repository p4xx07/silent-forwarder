import time
import telepot
import requests
import download
import os
import subprocess
import re
from logger import Logger
from telepot import Bot
from telepot.loop import MessageLoop
from config import getConfig
from random import randint
from PIL import Image
import json
class Handler():
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = getConfig()
        self.logger = Logger()
        self.token = self.config[0]
        self.channel_id = self.config[1]
        self.valid_users = self.config[2]
        self.active = True

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if str(chat_id) not in self.valid_users:
            self.logger.logWarn("user invalid\t" + str(chat_id))
            return
        if content_type == 'text':
            self.handleCommand(msg)
        elif content_type == 'photo':
            self.saveImage(msg)

    def handleCommand(self, msg):
        chat_id = msg['chat']['id']
        message = msg['text'].lower() 
        print(str(chat_id))
        if '/shutdown' in message:
            self.shutdown(chat_id)
        elif '/restart' in message:
            self.restart(chat_id)

    def saveImage(self, msg):
        chat_id = msg['chat']['id']
        infile = msg['photo']
        urlpath = self.bot.getFile(infile[-1]['file_id'])
        print(str(json.dumps(urlpath)))
        os.system('wget --no-check-certificate  ' + 'https://api.telegram.org/file/bot' + self.token + '\/' + urlpath['file_path'])
        filename = urlpath['file_path'].split('/')[-1]
        os.system('mv ' + filename + ' /opt/SilentForwarder/img')
        self.sendTextMessage(chat_id, filename)

    def sendImageToChannel(self):
        cmd = "ls -rt /opt/SilentForwarder/img | awk 'NR==1{print $1}'"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        stdout = ps.communicate()[0]
        outstr = stdout.decode("utf-8")
        if not outstr:
            return
        path = "/opt/SilentForwarder/img/" + outstr.rstrip("\n")
        image = open(path, "rb")
        print("opened " + path)
        print("sending to " + str(self.channel_id))
        self.sendImage(image, self.channel_id)
        os.system("rm " + path)
 
    def sendTextMessage(self, chat_id, message):
        self.bot.sendMessage(chat_id, message)

    def sendImage(self, image, chat_id):
        self.bot.sendPhoto(chat_id, photo=image)

    def shutdown(self, chat_id):
        self.sendTextMessage(chat_id, "Shutting down")
        self.active = False

    def restart(self, chat_id):
        self.sendTextMessage(chat_id, "Restarting down")
        self.active = True
