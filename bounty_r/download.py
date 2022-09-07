import time
from direc import *
from data import *

db=database()
conn=db.connect()
cur=conn.cursor()
def test(cid):
    sql = '''SELECT description FROM distribution WHERE id= %s '''
    cur.execute(sql % cid)
    a = cur.fetchone();
    return a[0]
def download(cid):
    sql = '''SELECT data FROM distribution WHERE id= %s '''
    cur.execute(sql % cid)
    a = cur.fetchone();
    if a[0]==None:
        return bytes(0)
    else:
        return bytes(a[0])
def overwrite(direc,data):
    a=open(direc,'wb')
    a.write(data)
    a.close()
def bbq(dire,cid):
    a=download(cid)
    overwrite(dire,a)
    return 'success'
a = input('input distribution id: \n')
print(test(a))
b= input('input bounty name (just exit if description above is not your aim)\n')+'.bin'
print(bbq(b,a))
print(f'check {b} in this folder')
time.sleep(2)
