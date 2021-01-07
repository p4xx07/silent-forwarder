import time
import telepot
import requests
import download
import restaurant
import meme
import os
import trim
import re
from logger import Logger
from telepot import Bot
from telepot.loop import MessageLoop
from restaurant import RestaurantFactory
from software import SoftwareFactory
from exclamation import ExclamationFactory
from answer import AnswerFactory
from config import getConfig
from random import randint
from PIL import Image
import json
class Handler():
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = getConfig()
        self.token = self.config[0]
        self.channel = self.config[1]
        self.valid_users = self.config[2]

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if not chat_in in self.valid_users:
            return
        if content_type == 'text':          
            self.handleCommand(msg)
        elif content_type == 'photo':          
            self.saveImage(msg)

    def handleCommand(self, msg):
        chat_id = msg['chat']['id']
        message = msg['text'].lower()

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
        os.system('mv ' + filename + ' /home/pi/Pictures/')
        self.sendTextMessage(chat_id, filename)

    def videoMessage(self, msg):
        chat_id = msg['chat']['id']
        video = msg['video']

        if int(video["file_size"]) > 3221225472: #3GB
            self.sendTextMessage(chat_id, "Not enough params!")
            return

        caption = "0 10"
        if 'caption' in msg:
            caption = msg['caption']
        
        split = caption.split()
        start = int(split[0])
        end = int(split[1])

        if len(split) != 2:
            self.sendTextMessage(chat_id, "Not enough params!")
            return

        if start < 0 or end < 0 or end - start < 0 or end - start > 10:
            self.sendTextMessage(chat_id, "Invalid params! Max 10 seconds of gif!")
            return

        if int(video["duration"]) < end:
            end = int(video["duration"])

        self.bot.sendChatAction(chat_id, "upload_video")
        download.downloadVideo(self.token, video["file_id"], "video.mp4")
        trim.trimVideoToGif("video.mp4", start, end)
        self.bot.sendChatAction(chat_id, "upload_video")
        self.sendTrimToGif(chat_id, "output.gif")

    def sendFoodGif(self):
        self.bot.sendVideo(self.chat_id, self.gif_url)
        #self.sendFoodMessage(self.config.chat_id)
        #self.sendRandomFact(self.config.chat_id)
        #self.sendRandomMeme(self.config.chat_id)
        #self.sendRandomJoke(self.chat_id)
        self.sendRandomAction()

    def sendRandomAction(self):
        rand = randint(0, 3)

        if rand == 0:
            self.sendTextMessage(self.chat_id, "Here's a random joke")
            self.sendRandomJoke(self.chat_id)
        elif rand == 1:
            self.sendTextMessage(self.chat_id, "Here's a random fact")
            self.sendRandomFact(self.chat_id)
        elif rand == 2:
            self.sendTextMessage(self.chat_id, "Here's a small harry potter chapter")
            self.sendRandomPotter(self.chat_id, 50)
        elif rand == 3:
            self.sendTextMessage(self.chat_id, "Here's a coding tip!")
            self.sendRandomSoftware(self.chat_id)

    def sendFoodMessage(self, chat_id):
        food = self.restaurantFactory.getFood()
        self.bot.sendMessage(chat_id, food)

    def sendRandomSoftware(self, chat_id):
        software = self.softwareFactory.getSoftware()
        self.bot.sendMessage(chat_id, software)

    def sendRandomAnswer(self, chat_id):
        answer = self.answerFactory.getAnswer()
        self.bot.sendMessage(chat_id, answer)

    def sendTextMessage(self, chat_id, message):
        self.bot.sendMessage(chat_id, message)

    def sendRandomFact(self, chat_id):
        f = requests.get('https://uselessfacts.jsph.pl/random.txt?language=en')
        text = f.text.split("\n")[0]
        text = text.replace("> ", "")
        self.bot.sendMessage(chat_id, text)

    def sendExclamation(self, chat_id):
        exclamation = self.exclamationFactory.getExclamation()
        self.bot.sendMessage(chat_id, exclamation)

    def sendRandomMeme(self, chat_id):
        image = meme.generateMeme()
        image.save("img.png")
        file = open('img.png', 'rb')
        self.bot.sendPhoto(chat_id, photo=file)

    def sendRandomTree(self, chat_id):
        import draw
        draw.generateTree()
        file = open('img/tree.gif', 'rb')
        self.bot.sendVideo(chat_id, video=file)

    def sendRoll(self, chat_id, sides: int):
        import roll
        value = roll.roll(sides)
        self.bot.sendMessage(chat_id, str(value))

        if(value == sides):
            self.bot.sendMessage(chat_id, "CRITICALLLLL!!!!")
        elif(value == 1):
            self.bot.sendMessage(chat_id, "RIP")

    def sendRandomJoke(self, chat_id):
        import joke
        value = joke.getRandomJoke()
        self.bot.sendMessage(chat_id, str(value))

    def sendTrimToGif(self, chat_id, path):
        file = open(path, 'rb')
        self.bot.sendDocument(chat_id, document=file)
        os.remove(path)

    def sendRandomPotter(self, chat_id, words=100):
        import markov
        if not self.potter_text:
            self.potter_text = markov.read_harry_potter()
        potter_file = markov.generate_text(self.potter_text, words)
        self.sendTextMessage(chat_id, potter_file)

    def sendWater(self):
        with open("/etc/food-picker/water.txt", encoding="utf8") as f:
            for line in f:
                if len(line.strip()) == 0:
                    continue
                self.bot.sendVideo(line, "https://media.tenor.com/images/a7eeadb549ca8b4f725a37d4e23ff2ce/tenor.gif")
                self.sendTextMessage(line, "Remember to drink some water!")

    def subscribeToWater(self, chat_id):
        found = False
        path = "/etc/food-picker/water.txt"
        with open(path, encoding="utf8") as f:
            for line in f:
                if line.strip() != str(chat_id):
                    continue
                found = True
        if found:
            self.unsubscribeFromWater(chat_id)
            return
        with open(path, 'a') as f:
            f.write('\n' + str(chat_id))
        self.sendTextMessage(chat_id, "Subscribed to water reminder")

    def unsubscribeFromWater(self, chat_id):
        path = "/etc/food-picker/water.txt"
        content = ""
        with open(path, "r" ) as f:
            lines = f.readlines()
        with open(path, "w") as f:
            for line in lines:
                if line.strip("\n") != str(chat_id) and len(line.strip()) > 0:
                    f.write(line)
        self.sendTextMessage(chat_id, "Unsubscribed to water reminder")
