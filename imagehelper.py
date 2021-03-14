import json
import subprocess
import os
import telegram.ext

def save_image(url, file_id):
    os.system('wget --no-check-certificate  ' + url)
    filename = url.split('/')[-1]
    os.system('mv ' + filename + ' /opt/SilentForwarder/img/')
    return filename

def get():
    cmd = "ls -rt /opt/SilentForwarder/img | awk 'NR==1{print $1}'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout = ps.communicate()[0]
    outstr = stdout.decode("utf-8")
    if not outstr:
        return
    path = "/opt/SilentForwarder/img/" + outstr.rstrip("\n")
    image = open(path, "rb")
    return (image, path)

def get_multiple(count):
    images = []
    paths = []
    for i in range(1, count + 1):
        cmd = "ls -rt /opt/SilentForwarder/img | awk 'NR==" + str(i) + "{print $1}'"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        stdout = ps.communicate()[0]
        outstr = stdout.decode("utf-8")
        if not outstr:
            return (images, paths)

        path = "/opt/SilentForwarder/img/" + outstr.rstrip("\n")
        paths.append(path)
        
        image = open(path.encode('utf-8'), "rb")
        media = telegram.InputMediaPhoto(media=image)
        images.append(media)
        

    return (images, paths)
