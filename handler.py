import time
import os
import random

from telegram import InputMediaVideo, InputMediaPhoto, InputMediaAnimation


active = True
base_url = None
valid_users = None
folder_path = "./media"


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
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Invalid command")


def restarted(bot):
    bot.send_message(chat_id=146470365, text="Restarted!")


def auth(chat_id) -> bool:
    global valid_users
    return str(chat_id) in valid_users


def save_media(update, context):
    if not auth(update.effective_chat.id):
        return
    file_id = -1
    media_type = "none"
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        media_type = "photo"
    elif update.message.video:
        file_id = update.message.video.file_id
        media_type = "video"
    elif update.message.document:
        file_id = update.message.document.file_id
        media_type = "document"
    elif update.message.audio:
        file_id = update.message.audio.file_id
        media_type = "audio"
    elif update.message.sticker:
        file_id = update.message.sticker.file_id
        media_type = "sticker"
    elif update.message.voice:
        file_id = update.message.voice.file_id
        media_type = "voice"
    elif update.message.animation:
        file_id = update.message.animation.file_id
        media_type = "animation"

    if file_id == -1:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="unable to process media type")
        return

    current_unix_time = int(time.time())
    random_number = random.randint(1111, 9999)
    filename = f"{media_type}_{random_number}_{current_unix_time}"
    file = open(folder_path+filename, 'w')
    file.write(file_id + "\n")
    file.close()

    context.bot.send_message(
        chat_id=update.effective_chat.id, text="saved media with id "+str(file_id))


def send_media_to_channel(bot, channel_id):
    media_file = get_first_media()
    if media_file == "":
        return
    parts = media_file.split("_", 1)
    media_type = parts[0]
    file = open(folder_path + media_file, 'r')
    file_id = file.readline().strip()
    file.close()

    if media_type == "photo":
        bot.send_photo(channel_id, file_id)
    elif media_type == "video":
        bot.send_video(channel_id, file_id)
    elif media_type == "animation":
        bot.send_animation(channel_id, file_id)

    os.remove(folder_path + media_file)


def send_medias_to_channel(bot, channel_id):
    media_files = get_first_n_media(5)
    if len(media_files) <= 0:
        return
    if len(media_files) == 1:
        send_media_to_channel(bot, channel_id)
        return

    medias = []
    for media_file in media_files:
        parts = media_file.split("_", 1)
        media_type = parts[0]
        file = open(folder_path + media_file, 'r')
        file_id = file.readline().strip()
        file.close()

        if media_type == "photo":
            p = InputMediaPhoto(media=file_id)
            medias.append(p)
        elif media_type == "video":
            v = InputMediaVideo(media=file_id)
            medias.append(v)
        elif media_type == "animation":
            an = InputMediaAnimation(media=file_id)
            medias.append(an)

    try:
        bot.send_media_group(chat_id=channel_id, media=medias)

    except Exception as ex:
        print(ex)

    for media_file in media_files:
        os.remove(folder_path + media_file)


def reminder(bot, channel_id):
    global active
    last_epoch = time.time()
    while True:
        if active is False:
            time.sleep(5)
            continue
        if (time.time() - last_epoch >= 60 * 30):
            send_media_to_channel(bot, channel_id)
            # send_medias_to_channel(bot, channel_id)
            last_epoch = time.time()
            time.sleep(5)
            continue


def get_first_media():
    try:
        file_list = os.listdir(folder_path)
        if not file_list:
            return ""
        file_list = [file for file in file_list if os.path.isfile(
            os.path.join(folder_path, file))]
        oldest_file = min(file_list, key=lambda x: os.path.getmtime(
            os.path.join(folder_path, x)))
        return oldest_file
    except Exception as ex:
        print(f"Error: {ex}")
        return ""


def get_first_n_media(num_files=1):
    try:
        file_list = os.listdir(folder_path)
        if not file_list:
            return ""
        file_list = [file for file in file_list if os.path.isfile(
            os.path.join(folder_path, file))]
        oldest_files = sorted(file_list, key=lambda x: os.path.getmtime(
            os.path.join(folder_path, x)))[:num_files]
        return oldest_files
    except OSError as ex:
        print(f"Error: {ex}")
        return []
