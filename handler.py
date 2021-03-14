import datetime
import time
import imagehelper as ImageHelper
import os
active = True
base_url = None
valid_users = None

def set_valid_users(users):
    global valid_users
    valid_users = users

def start(update, context):
    global active
    if not auth(update.effective_chat.id):
        return
    active = True
    context.bot.send_message(chat_id=update.effective_chat.id, text="Started")

def stop(update, context):
    global active
    if not auth(update.effective_chat.id):
        return
    active = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="Stopped")

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command")

def restarted(bot):
    bot.send_message(chat_id=146470365, text="Restarted!")

def auth(chat_id) -> bool:
    global valid_users
    return str(chat_id) in valid_users 

def save_image(update, context):
    if not auth(update.effective_chat.id):
        return
    photo = update.message.photo[-1]
    photo_file = photo.get_file()
    url = photo_file["file_path"]
    filename = ImageHelper.save_image(url, photo_file["file_id"])
    context.bot.send_message(chat_id=update.effective_chat.id, text=filename)

def send_image_to_channel(bot, channel_id):
    (image, path) = ImageHelper.get()
    bot.send_photo(channel_id, image)
    return
    os.system("rm " + path)

def send_images_to_channel(bot, channel_id):
    (images, paths) = ImageHelper.get_multiple(10)
    bot.send_media_group(channel_id, images)
    return
    for path in paths:
        os.system("rm " + path)

def reminder(bot, channel_id):
    global active
    last_epoch = time.time()
    while True:
        if active is False:
            time.sleep(5)
            continue
        if(time.time() - last_epoch >= 5 * 1):
            send_images_to_channel(bot, channel_id)
            last_epoch = time.time()
            continue

