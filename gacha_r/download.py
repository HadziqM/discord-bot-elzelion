from direc import *
from data import *


class DownLoad():
    def __init__(self):
        db = database()
        self.conn = db.connect()
        self.cur = self.conn.cursor()
        self.sql = '''SELECT description FROM distribution WHERE id= %s '''
        self.sql1 = '''SELECT data FROM distribution WHERE id= %s '''

    def get(self, dir, cid):
        self.cur.execute(self.sql1 % cid)
        a = self.cur.fetchone()
        if a[0] == None:
            return print("no data")
        else:
            bty = bytes(a[0])
            dat = open(dir, 'wb')
            dat.write(bty)
            dat.close()
            return print("success")

    def print(self, cid, dir):
        # a = input('input distribution id: \n')
        a = cid
        self.cur.execute(self.sql % a)
        print(self.cur.fetchone()[0])
        # b = input('input bounty name (just exit if description above is not your aim)\n')+'.bin'
        b = dir
        return self.get(b, a)


def connect():
    db = database()
    conn = db.connect()
    cur = conn.cursor()
    return cur


def test(cid, cur):
    sql = '''SELECT description FROM distribution WHERE id= %s '''
    cur.execute(sql % cid)
    a = cur.fetchone()
    return a[0]


def download(cid, cur):
    sql = '''SELECT data FROM distribution WHERE id= %s '''
    cur.execute(sql % cid)
    a = cur.fetchone()
    if a[0] == None:
        return bytes(0)
    else:
        return bytes(a[0])


def overwrite(direc, data):
    a = open(direc, 'wb')
    a.write(data)
    a.close()


def bbq(dire, cid, cur):
    a = download(cid, cur)
    overwrite(dire, a)
    return 'success'


def interact():
    cur = connect()
    a = input('input distribution id: \n')
    print(test(a, cur))
    b = input(
        'input bounty name (just exit if description above is not your aim)\n')+'.bin'
    print(bbq(b, a, cur))
    print(f'check {b} in this folder')


down = DownLoad()
down.print()
