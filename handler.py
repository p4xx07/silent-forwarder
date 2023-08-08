import datetime
import time
import mediaHelper as MediaHelper
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

def restart(update, context):
    global active
    if not auth(update.effective_chat.id):
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text="Restarting")
    os.system("sudo systemctl restart silent_forwarder")

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command")

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
            file_id = media.photo[-1].file_id
            media_type = "photo"
        elif update.message.video:
            file_id = media.video.file_id
            media_type = "video"
        elif update.message.document:
            file_id = media.document.file_id
            media_type = "document"
        elif update.message.audio:
            file_id = media.audio.file_id
            media_type = "audio"
        elif update.message.sticker:
            file_id = media.sticker.file_id
            media_type = "sticker"
        elif update.message.voice:
            file_id = media.voice.file_id
            media_type = "voice"
        elif update.message.animation:
            file_id = media.animation.file_id
            media_type = "animation"

    if file_id == -1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="unable to process media type")
        return

    open("/opt/SilentForwarder/media/"+file_id+"_"+media_type, 'w') as file:
        pass

    context.bot.send_message(chat_id=update.effective_chat.id, text="saved media with id "+str(file_id))

def send_media_to_channel(bot, channel_id):
    media_file = get_first_media()
    parts = media_file.split("_", 1)
    file_id = parts[0]
    media_type = parts[1]
    if media_type == "photo":
        bot.send_photo(channel_id, file_id)
    elif media_type == "video":
        bot.send_video(channel_id, file_id)
    elif media_type == "document":
        bot.send_document(channel_id, file_id)
    elif media_type == "audio":
        bot.send_audio(channel_id, file_id)
    elif media_type == "sticker":
        bot.send_sticker(channel_id, file_id)
    elif media_type == "voice":
        bot.send_voice(channel_id, file_id)
    elif media_type == "animation":
        bot.send_animation(channel_id, file_id)

    print("trying to remove: " + media_file)
    os.remove(media_file)

def send_medias_to_channel(bot, channel_id):
    try:
        media_files = get_first_n_media(5)
        if len(medias) <= 0:
            return
        if len(medias) == 1:
            send_media_to_channel(bot, channel_id)
            return

        medias = []
        for media_file in media_files:
            parts = media_file.split("_", 1)
            file_id = parts[0]
            media_type = parts[1]

            if media_type == "photo":
                p = ImageMediaPhoto(media=file_id)
                medias.append(p)
            elif media_type == "video":
                v = ImageMediaVideo(media=file_id)
                medias.append(v)
            elif media_type == "document":
                d = ImageMediaDocument(media=file_id)
                medias.append(d)
            elif media_type == "audio":
                a = ImageMediaAudio(media=file_id)
                medias.append(a)
            elif media_type == "sticker":
                s = ImageMediaSticker(media=file_id)
                medias.append(s)
            elif media_type == "voice":
                vc = ImageMediaVoice(media=file_id)
                medias.append(vc)
            elif media_type == "animation":
                a = ImageMediaAnimation(media=file_id)
                medias.append(a)

        bot.send_media_group(chat_id=chat_id, media=medias)

        for path in paths:
            print("trying to remove: " + media_file)
            os.remove(medias)

    except Exception as e:
        print("lolol something went wrong")
        print(e)

def reminder(bot, channel_id):
    global active
    last_epoch = time.time()
    while True:
        if active is False:
            time.sleep(5)
            continue
        if(time.time() - last_epoch >= 60 * 30):
            send_media_to_channel(bot, channel_id)
            last_epoch = time.time()
            time.sleep(5)
            continue


def get_first_media():
    folder_path = '/etc/SilentForwarder/media'
    file_list = os.listdir(folder_path)
    file_list = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file))]
    oldest_file = min(file_list, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    oldest_file_path = os.path.join(folder_path, oldest_file)
    return oldest_file

def get_first_n_media(num_files=1):
    folder_path = '/etc/SilentForwarder/media'
    try:
        file_list = os.listdir(folder_path)
        file_list = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file))]
        oldest_files = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))[:num_files]

        oldest_files_paths = [os.path.join(folder_path, file) for file in oldest_files]

        return oldest_files_paths
    except OSError as e:
        print(f"Error: {e}")
        return []
