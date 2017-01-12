#!/usr/bin/env python

import configparser
import webbrowser
from os.path import expanduser
import os.path
import sys

from imgurpython import ImgurClient

if len(sys.argv) != 2:
    print("Usage: %s <image file>" % sys.argv[0])
    sys.exit(1)

# imgur-up tokens
# see: https://api.imgur.com/oauth2
client_id = CHANGE_ME
client_secret = CHANGE_ME
access_token = None
refresh_token = None

# client
client = ImgurClient(client_id, client_secret)


def get_tokens_path():
    home = expanduser("~")
    tokens_path = home + '/.imgur-up'
    return tokens_path


def load_tokens():
    global access_token, refresh_token

    if os.path.isfile(get_tokens_path()):
        config = configparser.ConfigParser()

        config.read(get_tokens_path())

        access_token = config['tokens']['access_token']
        refresh_token = config['tokens']['refresh_token']


def set_client_tokens():
    client.set_user_auth(access_token, refresh_token)


def save_tokens():
    config = configparser.ConfigParser()
    config['tokens'] = {}
    config['tokens']['access_token'] = access_token
    config['tokens']['refresh_token'] = refresh_token

    with open(get_tokens_path(), 'w') as configfile:
        config.write(configfile)


def get_credentials():
    authorization_url = client.get_auth_url('pin')

    webbrowser.open_new_tab(authorization_url)

    pin = input("pin? ")

    return client.authorize(pin, 'pin')


def get_new_tokens():
    global access_token, refresh_token

    credentials = get_credentials()
    access_token = credentials['access_token']
    refresh_token = credentials['refresh_token']

    # persist
    save_tokens()


# ########### main ###############

# try and load existing tokens
load_tokens()

# if none found, get some new ones
if access_token is None and refresh_token is None:
    get_new_tokens()

# set tokens in existing client
set_client_tokens()

response = client.upload_from_path(sys.argv[1], anon=False)

link = response['link']

print(link)

webbrowser.open_new_tab(link)
