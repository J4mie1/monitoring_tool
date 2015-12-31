#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5
print("Content-Type: text/html; charset=utf-8\n")

from lib import classes

config = classes.functions.leesXMLConfig("config.xml", "r", "SV02")



debuglijst = []
debuglijst.append(__file__ + " gestart...")

"""
# settings
host                = '192.168.34.184'
port                = "8888"
ww                  = "jamie"
OS                  = "L"   # kies W of L
genereer_grafieken  = 1
voegtoe_aan_csv     = 1
locatie             = "/Applications/XAMPP/xamppfiles/htdocs/monitoringtool/"
locatie_grafieken   = "grafieken/" # met slash
csv_file        = "metingen.csv"
database_file   = "lib/monitoringtool.sqlite"
logfile             = "log/SV02.txt"
genereer_logging    = 1
"""

agent = classes.Agent(config[1]["host"], config[1]["port"], config[1]["ww"], config[1]["OS"], classes.functions.geefDatum(), config[0]["locatie"], config[0]["locatie_grafieken"], config[0]["database_file"])

from lib.layout import head
from lib.layout import menu1
print("""
                    <li><a href="index.py">SV01</a></li>
                    <li class="active"><a href="#">SV02</a></li>""")
from lib.layout import menu2

agent_connect = agent.verbindingOpzetten()
if config[1]["OS"] == "W" or config[1]["OS"] == "L":

    if agent_connect == 1:
        print("""
        <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
            <div class="alert alert-warning">Error: Host """ + config[1]["host"] + """ is te pingen, maar:
                <ul>
                    <li>Controleer of het agent script draait</li>
                    <li>Controleer of het poortnummer aan beide kanten klopt</li>
                </ul>
            </div>
        </div>""")
        debuglijst.append("Error: kan niet verbinden naar agent " + config[1]["host"] + ":" + config[1]["port"] + " (code 1)")

    elif agent_connect == 2:
        print("""
        <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
            <div class="alert alert-warning">
                Error: Host """ + config[1]["host"] + """ kon niet worden benaderd, controleer het IP-adres
            </div>
        </div>""")
        debuglijst.append("Error: kan niet verbinden naar agent " + config[1]["host"] + ":" + config[1]["port"] + " (code 2)")

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
        debuglijst.append("Verbinding gemaakt met agent " + config[1]["host"] + ":" + config[1]["port"] +", counters succesvol opgehaald")

        if config[1]["OS"] == "W":
                    counters.append(agent.geefRunningServices())
                    counters.append(agent.geefStoppedServices())
                    counters.append(agent.geefTotalServices())

        agent.verlaatSessie()
        debuglijst.append("Verbinding met agent " + config[1]["host"] + ":" + config[1]["port"] + " weer verbroken")
        host_id = agent.genereerHostID()

        if int(config[1]["genereer_grafieken"]) == 1 and int(config[1]["voegtoe_aan_csv"]) == 1:
            grafieken = [   agent.genereerGrafiek(1, counters[5][1], classes.functions.geefTijdInDecimalen()),
                            agent.bewaarInCsv(config[0]["csv_file"]),
                            agent.genereerGrafiek(2, counters[13], classes.functions.geefTijdInDecimalen()),
                            agent.bewaarInCsv(config[0]["csv_file"]),
                            agent.genereerGrafiek(3, counters[14], classes.functions.geefTijdInDecimalen()),
                            agent.bewaarInCsv(config[0]["csv_file"])
                            ]
            debuglijst.append("Grafieken gegenereerd")
            debuglijst.append("Processorbelasting, datagebruik en geheugengebruik counters toegevoegd aan " + config[0]["csv_file"])

        elif int(config[1]["genereer_grafieken"]) == 1 and int(config[1]["voegtoe_aan_csv"]) == 0:
            grafieken = [   agent.genereerGrafiek(1, counters[5][1], classes.functions.geefTijdInDecimalen()),
                            agent.genereerGrafiek(2, counters[13], classes.functions.geefTijdInDecimalen()),
                            agent.genereerGrafiek(3, counters[14], classes.functions.geefTijdInDecimalen())
                            ]
            debuglijst.append("Grafieken gegenereerd")

        elif int(config[1]["genereer_grafieken"]) == 0 and int(config[1]["voegtoe_aan_csv"]) == 1:
            agent.bewaarAlleenInCsv(counters[5][1], counters[13], counters[14], str(classes.functions.geefTijdInDecimalen(), config[0]["csv_file"]))
            debuglijst.append("Processorbelasting, datagebruik en geheugengebruik counters toegevoegd aan " + config[0]["csv_file"])

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

        if config[1]["OS"] == "W":
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
            alle_grafieken.append((grafiek_id, i[1], "Gemeten processorbelasting"))

        print("""
                            <li role="presentation" class="divider"></li>
                            <li role="presentation" class="dropdown-header">Datagebruik</li>""")

        for i in agent.genereerDropdown()[1]:
            grafiek_id = agent.geefGrafiekID(i[0], 2, host_id)
            print("""
                            <li role='presentation'><a role='menuitem' tabindex='-1' data-toggle='modal' data-target='#""" + grafiek_id + """'>""" + i[0] + """</a></li>""")
            if config[1]["OS"] == "W":
                alle_grafieken.append((grafiek_id, i[1], "Datagebruik C:"))
            else:
                alle_grafieken.append((grafiek_id, i[1], "Datagebruik /dev/sda1"))

        print("""
                            <li role="presentation" class="divider"></li>
                            <li role="presentation" class="dropdown-header">Geheugengebruik</li>""")

        for i in agent.genereerDropdown()[2]:
            grafiek_id = agent.geefGrafiekID(i[0], 3, host_id)
            print("""
                            <li role='presentation'><a role='menuitem' tabindex='-1' data-toggle='modal' data-target='#""" + grafiek_id + """'>""" + i[0] + """</a></li>""")
            alle_grafieken.append((grafiek_id, i[1], "Geheugengebruik"))

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
    debuglijst.append("Error: optie 'OS' mag alleen 'W' of 'L' zijn")

from lib.layout import footer
debuglijst.append("____________________________________________________________________________________________________________" + "\n")

if int(config[1]["genereer_logging"]) == 1:
    agent.schrijfNaarLogFile(config[1]["logfile"], debuglijst)

classes.functions.uploadNaarGitHub(__file__)