#! /usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/HBR/")

from HBR import app as application
application.secret_key = "This is a secret!!! Do nOt disclose!!!"
