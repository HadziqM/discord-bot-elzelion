import psycopg2
from configparser import ConfigParser
from definition import *


def config(section, filename=CONFIG_PATH):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


class database:
    def __init__(self):
        a = config('discord')
        self.param = config('postgresql')
        self.token = a['token']
        self.mod = a['moderator']
        self.cd = a['cooldown']
        self.announce = a['announcement']
        self.leaderboard = a['leaderboard']
        self.promotion = a['promotion']
        self.road = a['roadrole']
        self.elze = a['elzerole']
        self.champion = a['championrole']
        self.master = a['masterrole']
        self.expert = a['expertrole']
        self.error = a['error']
        self.p1 = a['game_p1']
        self.p2 = a['game_p2']
        self.rolep1 = a['game_p1_role']
        self.rolep2 = a['game_p2_role']
        self.game = a['game_announce']
        b = a['command']
        b = [i for i in b]
        for i in range(len(b)):
            if b[i] == '_':
                b[i] = ' '
        self.command = ''.join(b)

    def connect(self):
        global conn, cur
        conn = psycopg2.connect(**self.param)
        cur = conn.cursor()
        print('connected')
        return conn
