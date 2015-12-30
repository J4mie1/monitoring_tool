#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5
print("Content-Type: text/html; charset=utf-8\n")

from lib import classes
from subprocess import call, Popen, PIPE
import subprocess
import os
import git


# settings
host                = '192.168.34.179'
port                = 8888
ww                  = "jamie"
OS                  = "L"   # kies W of L
genereer_grafieken  = 1
csv                 = 1
locatie             = "/Applications/XAMPP/xamppfiles/htdocs/monitoringtool/"
locatie_grafieken   = "grafieken/" # met slash
pad_naar_csv        = "metingen.csv"
pad_naar_database   = "lib/monitoringtool.sqlite"

agent = classes.Agent(host, port, ww, OS, classes.functions.geefDatum(), locatie, locatie_grafieken, pad_naar_database)

from lib.layout import head
from lib.layout import menu1
print("""
                    <li><a href="index.py">SV01</a></li>
                    <li class="active"><a href="#">SV02</a></li>""")
from lib.layout import menu2

agent_connect = agent.verbindingOpzetten()
if OS == "W" or OS == "L":

    if agent_connect == 1:
        print("""
        <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
            <div class="alert alert-warning">Error: Host """ + host + """ is te pingen, maar:
                <ul>
                    <li>Controleer of het agent script draait</li>
                    <li>Controleer of het poortnummer aan beide kanten klopt</li>
                </ul>
            </div>
        </div>""")

    elif agent_connect == 2:
        print("""
        <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
            <div class="alert alert-warning">
                Error: Host """ + host + """ kon niet worden benaderd, controleer het IP-adres
            </div>
        </div>""")

    else:
        counters = [agent.geefHostname(),           #0
                    agent.geefOS(),                 #1
                    agent.geefIP(),                 #2
                    agent.geefUsers(),              #3
                    agent.geefUptime(),             #4
                    agent.geefCPULoad(),            #5 [0] voor string, [1] voor float
                    agent.geefRunningProcesses(),   #6
                    agent.geefAMemory(),            #7
                    agent.geefTMemory(),            #8
                    agent.geefDriveLabel(),         #9
                    agent.geefFileSystem(),         #10
                    agent.geefACapacity(),          #11
                    agent.geefTCapacity(),          #12
                    agent.geefUCapacity(),          #13
                    agent.geefUMemory()             #14
                    ]

        if OS == "W":
                    counters.append(agent.geefRunningServices())
                    counters.append(agent.geefStoppedServices())
                    counters.append(agent.geefTotalServices())

        agent.verlaatSessie()
        host_id = agent.genereerHostID()

        if genereer_grafieken == 1 and csv == 1:
            grafieken = [   agent.genereerGrafiek(1, counters[5][1], classes.functions.geefTijdInDecimalen()),
                            agent.bewaarInCsv(pad_naar_csv),
                            agent.genereerGrafiek(2, counters[13], classes.functions.geefTijdInDecimalen()),
                            agent.bewaarInCsv(pad_naar_csv),
                            agent.genereerGrafiek(3, counters[14], classes.functions.geefTijdInDecimalen()),
                            agent.bewaarInCsv(pad_naar_csv)
                            ]

        elif genereer_grafieken == 1 and csv == 0:
            grafieken = [   agent.genereerGrafiek(1, counters[5][1], classes.functions.geefTijdInDecimalen()),
                            agent.genereerGrafiek(2, counters[13], classes.functions.geefTijdInDecimalen()),
                            agent.genereerGrafiek(3, counters[14], classes.functions.geefTijdInDecimalen())
                            ]

        elif genereer_grafieken == 0 and csv == 1:
            agent.bewaarAlleenInCsv(counters[5][1], counters[13], counters[14], str(classes.functions.geefTijdInDecimalen(), pad_naar_csv))

        print("""
            <div class="row small">
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6 small">
                    <h4>Overzicht</h4>
                    <div class="table-responsive">
                        <table class="table table-striped table-condensed">
                            <thead>
                                <tr>
                                    <td><strong>Systeem</strong></td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Hostname:</td>
                                    <td>""" + counters[0] + """</td>
                                </tr>
                                <tr>
                                    <td>OS:</td>
                                    <td>""" + counters[1] + """</td>
                                </tr>
                                <tr>
                                    <td>IP-adres:</td>
                                    <td>""" + counters[2] + """</td>
                                </tr>
                                <tr>
                                    <td>Ingelogde gebruiker(s):</td>
                                    <td>""" + counters[3] + """</td>
                                </tr>
                                <tr>
                                    <td>Uptime:</td>
                                    <td>""" + counters[4] + """</td>
                                </tr>
                                <tr>
                                    <td><strong>CPU</strong></td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>Processorbelasting:</td>
                                    <td>""" + counters[5][0] + """</td>
                                </tr>
                                <tr>
                                    <td>Aantal draaiende processen:</td>
                                    <td>""" + counters[6] + """</td>
                                </tr>
                                <tr>
                                    <td><strong>Geheugen</strong></td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>Beschikbaar geheugen:</td>
                                    <td>""" + counters[7] + """</td>
                                </tr>
                                <tr>
                                    <td>Totaal geheugen:</td>
                                    <td>""" + counters[8] + """</td>
                                </tr>
                                <tr>
                                    <td><strong>Opslag</strong></td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>Label:</td>
                                    <td>""" + counters[9] + """</td>
                                </tr>
                                <tr>
                                    <td>Bestandssysteem:</td>
                                    <td>""" + counters[10] + """</td>
                                </tr>
                                <tr>
                                    <td>Beschikbare capaciteit:</td>
                                    <td>""" + counters[11] + """</td>
                                </tr>
                                <tr>
                                    <td>Totale capaciteit:</td>
                                    <td>""" + counters[12] + """</td>
                                </tr>""")

        if OS == "W":
            print("""
                                <tr>
                                    <td><strong>Services</strong></td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>Aantal draaiende services:</td>
                                    <td>""" + counters[13] + """</td>
                                </tr>
                                <tr>
                                    <td>Aantal gestopte services:</td>
                                    <td>""" + counters[14] + """</td>
                                </tr>
                                <tr>
                                    <td>Totaal aantal services:</td>
                                    <td>""" + counters[15] + """</td>
                                </tr>""")

        print("""
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    <h4>Metingen</h4>
                    <div class="btn-group">
                        <button type="button" class="btn btn-info dropdown-toggle btn-xs" data-toggle="dropdown">
                            Kies grafiek
                            <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
                            <li role="presentation" class="dropdown-header">Processorbelasting</li>""")

        alle_grafieken = []

        for i in agent.genereerDropdown()[0]:
            grafiek_id = agent.geefGrafiekID(i[0], 1, host_id)
            print("""
                            <li role='presentation'><a role='menuitem' tabindex='-1' data-toggle='modal' data-target='#""" + grafiek_id + """'>""" + i[0] + """</a></li>""")
            value = (grafiek_id, i[1], "Gemeten processorbelasting")
            alle_grafieken.append(value)

        print("""
                            <li role="presentation" class="divider"></li>
                            <li role="presentation" class="dropdown-header">Datagebruik</li>""")

        for i in agent.genereerDropdown()[1]:
            grafiek_id = agent.geefGrafiekID(i[0], 2, host_id)
            print("""
                            <li role='presentation'><a role='menuitem' tabindex='-1' data-toggle='modal' data-target='#""" + grafiek_id + """'>""" + i[0] + """</a></li>""")
            if OS == "W":
                value = (grafiek_id, i[1], "Datagebruik C:")
            else:
                value = (grafiek_id, i[1], "Datagebruik /dev/sda1")
            alle_grafieken.append(value)

        print("""
                            <li role="presentation" class="divider"></li>
                            <li role="presentation" class="dropdown-header">Geheugengebruik</li>""")

        for i in agent.genereerDropdown()[2]:
            grafiek_id = agent.geefGrafiekID(i[0], 3, host_id)
            print("""
                            <li role='presentation'><a role='menuitem' tabindex='-1' data-toggle='modal' data-target='#""" + grafiek_id + """'>""" + i[0] + """</a></li>""")
            value = (grafiek_id, i[1], "Geheugengebruik")
            alle_grafieken.append(value)

        print("""
                        </ul>
                    </div>
                </div>
            </div>""")

        for i in alle_grafieken:
            print("""
            <div class="modal fade" id='""" + i[0] + """' tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                                &times;
                            </button>
                            <h4 class="modal-title" id="myModalLabel">""" + i[2] + """</h4>
                        </div>
                        <div class="modal-body">
                            <img class="center-block img-responsive img-rounded" src='""" + i[1] + """'>
                        </div>
                    </div>
                </div>
            </div>""")

else:
    print("""
            <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                <div class="alert alert-danger">Error: Optie "OS" mag alleen "W" of "L" bevatten</div>
            </div>""")

from lib.layout import footer



# ohai




filenaam = __file__
import debug
devnull = open('/dev/null', 'w')

"""

call('git init --exec-path=/usr/local/git/bin/', stdout=devnull, stderr=devnull, shell=True)
call("git add " + str(filenaam), stdout=devnull, stderr=devnull, shell=True)
call("git commit -m 'commit'", stdout=devnull, stderr=devnull, shell=True)
call("git pull origin master", stdout=devnull, stderr=devnull, shell=True)
call("git remote add origin https://github.com/J4mie1/monitoring_tool.git", stdout=devnull, stderr=devnull, shell=True)
call("git push -u origin master", stdout=devnull, stderr=devnull, shell=True)
"""

#call(['git', 'init', ' --exec-path=/usr/local/git/bin/'])
p = Popen(['/usr/local/git/bin/git', "init"], stdout=PIPE, stderr=PIPE)
print (p.communicate())
print(" ")
p = Popen(['/usr/local/git/bin/git', "add", str(filenaam)], stdout=PIPE, stderr=PIPE)
print (p.communicate())
print(" ")
p = Popen(['/usr/local/git/bin/git', "commit", "-m" ,'commit'], stdout=PIPE, stderr=PIPE)
print (p.communicate())
print(" ")
p = Popen(['/usr/local/git/bin/git', "pull", "origin", "master"], stdout=PIPE, stderr=PIPE)
print (p.communicate())
print(" ")
p = Popen(['/usr/local/git/bin/git', "remote", "add", "origin", "https://github.com/J4mie1/monitoring_tool.git"], stdout=PIPE, stderr=PIPE)
print (p.communicate())
print(" ")
p = Popen(['/usr/local/git/bin/git', "push", "-u", "origin", "master"], stdout=PIPE, stderr=PIPE)
print (p.communicate())
print(" ")

print(devnull)

# een aantal bewerkingen


print(__file__)

# weer een testjesdfsdf
# sfsdfsfdfs
