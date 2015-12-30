__author__ = 'jamie'

#gecontroleerd

import socket
from datetime import datetime
from subprocess import Popen, PIPE

s = socket.socket()
s.settimeout(10)

def verstuurData(data):
    try:
        s.send(data.encode())
    except BrokenPipeError:
        return 0

def ontvangData():
    data = s.recv(1024)
    data = data.decode('ascii') # Er zijn bytes ontvangen, maak daar een string van
    data = data.rstrip()        # Verwijder \r | \n | \r\n
    return data

def byteNaarGB(aantal):
    aantal_i = int(aantal)
    return aantal_i/1024**3

def byteNaarMB(aantal):
    aantal_i = int(aantal)
    return aantal_i//1024**2

def geefDatum():
    tijd = str(datetime.now())[0:10]
    value = ""
    for i in tijd:
        if i == "-":
            pass
        else:
            value += i
    return int(value)

def datumNaarTekst(datum):
    dag = str(datum)[6:]
    mnd = str(datum)[4:6]
    jaar = str(datum)[0:4]

    maanden = {"01": "jan",
               "02": "feb",
               "03": "mrt",
               "04": "apr",
               "05": "mei",
               "06": "jun",
               "07": "jul",
               "08": "aug",
               "09": "sep",
               "10": "okt",
               "11": "nov",
               "12": "dec"}

    dag_vd_week = datetime.weekday(datetime(int(jaar),int(mnd),int(dag)))

    dagen =    {0: "ma",
                1: "di",
                2: "wo",
                3: "do",
                4: "vr",
                5: "za",
                6: "zo"}

    return dagen[dag_vd_week] + " " + dag + " " + maanden[mnd] + " " + jaar

def tekstNaarDatum(datum):
    dag = datum[3:5]
    mnd = datum[6:9]
    jaar = datum[10:14]

    maanden = {"01": "jan",
               "02": "feb",
               "03": "mrt",
               "04": "apr",
               "05": "mei",
               "06": "jun",
               "07": "jul",
               "08": "aug",
               "09": "sep",
               "10": "okt",
               "11": "nov",
               "12": "dec"}

    for i in maanden.items():
        if i[1] == mnd:
            mnd = i[0]

    return int(jaar + mnd + dag)

def geefTijdInDecimalen():
    tijd = str(datetime.now())[11:-7]
    h, m, s = [int(i) for i in tijd.split(':')]
    minuten_in_seconden = m * 60
    minuten_in_seconden_en_gewone_seconden = minuten_in_seconden + s
    aantal_minuten_in_procent = minuten_in_seconden_en_gewone_seconden / 3600
    amip_f = "%0.2f" % aantal_minuten_in_procent
    return float(amip_f) + h

def geefTijdInSeconden():
    tijd = str(datetime.now())[11:-7]
    h, m, s = [int(i) for i in tijd.split(':')]
    uren_in_seconden = h*60*60
    minuten_in_seconden = m*60
    return uren_in_seconden+minuten_in_seconden+s

def tijdInDecimalenNaarGewoon(tijd):
    t1 = tijd.split('.')
    uren = t1[0]
    min = (int(t1[1]) / 100) * 60
    return str(uren) + ":" + str(min)

def uploadNaarGitHub(file):
    debug = 0
    if debug == 1:
        p = Popen(['/usr/local/bin/git', "init"], stdout=PIPE, stderr=PIPE)
        print (p.communicate())
        p = Popen(['/usr/local/bin/git', "add", str(file)], stdout=PIPE, stderr=PIPE)
        print (p.communicate())
        p = Popen(['/usr/local/bin/git', "commit", "-m" ,'commit'], stdout=PIPE, stderr=PIPE)
        print (p.communicate())
        p = Popen(['/usr/local/bin/git', "pull", "origin", "master"], stdout=PIPE, stderr=PIPE)
        print (p.communicate())
        p = Popen(['/usr/local/bin/git', "remote", "add", "origin", "https://github.com/J4mie1/monitoring_tool.git"], stdout=PIPE, stderr=PIPE)
        print (p.communicate())
        p = Popen(['/usr/local/bin/git', "push", "-u", "origin", "master"], stdout=PIPE, stderr=PIPE)
        print (p.communicate())

    else:
        p = Popen(['/usr/local/bin/git', "init"], stdout=PIPE, stderr=PIPE)
        p.communicate()
        p = Popen(['/usr/local/bin/git', "add", str(file)], stdout=PIPE, stderr=PIPE)
        p.communicate()
        p = Popen(['/usr/local/bin/git', "commit", "-m" ,'commit'], stdout=PIPE, stderr=PIPE)
        p.communicate()
        p = Popen(['/usr/local/bin/git', "pull", "origin", "master"], stdout=PIPE, stderr=PIPE)
        p.communicate()
        p = Popen(['/usr/local/bin/git', "remote", "add", "origin", "https://github.com/J4mie1/monitoring_tool.git"], stdout=PIPE, stderr=PIPE)
        p.communicate()
        p = Popen(['/usr/local/bin/git', "push", "-u", "origin", "master"], stdout=PIPE, stderr=PIPE)
        p.communicate()

uploadNaarGitHub(__file__)
