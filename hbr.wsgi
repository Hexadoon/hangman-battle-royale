#! /usr/bin/python3.8

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/hangman-battle-royale/")

from hangman-battle-royale import app as application
application.secret_key = "This is a secret!!! Do nOt disclose!!!"
