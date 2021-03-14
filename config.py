import os
def readConfig(path) -> {}:
    d = {}
    with open(path) as f:
        for line in f:
            (key, val) = line.split("=")
            d[key] = val.replace('\n', '')
    return d

def get(): 
    config_path = "/etc/SilentForwarder/config.dat"

    if os.name == 'nt':
        config_path = r'C:\Users\pc\Documents\etc\food-picker\config.dat'

    config_dictionary = readConfig(config_path)

    token = config_dictionary["token"]
    channel_id = config_dictionary["channel_id"]
    valid_users = config_dictionary["valid_users"].split(",")
    return (token, channel_id, valid_users)
