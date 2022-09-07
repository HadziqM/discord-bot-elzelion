import quart
import os
import requests
from direc import *

app = quart.Quart("")
app.secret_key = bytes(str(os.urandom(24)), "utf-8")
