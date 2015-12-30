__author__ = 'jamie'

# gecontroleerd

from lib import functions
import sqlite3, cgitb, socket, csv
import numpy as np
import matplotlib.pyplot as plt

cgitb.enable()

class Agent:

    def __init__(self, host, port, ww, OS, datum, locatie, locatie_grafieken, conn):
        # constructor
        self.host               = host
        self.port               = port
        self.ww                 = ww
        self.OS                 = OS
        self.datum              = datum
        self.locatie            = locatie
        self.locatie_grafieken  = locatie_grafieken
        self.conn = sqlite3.connect(conn)

        # client commands
        self.hostname           = "hostname"
        self.os                 = "os"
        self.ip_address         = "ip_address"
        self.logged_on_users    = "logged_on_users"
        self.drive_label        = "drive_label"
        self.file_system        = "file_system"
        self.a_capacity         = "a_capacity"
        self.t_capacity         = "t_capacity"
        self.running_processes  = "running_processes"
        self.cpu_load           = "cpu_load"
        self.uptime             = "uptime"
        self.a_memory           = "a_memory"
        self.t_memory           = "t_memory"
        self.stop               = "stop"

        # client commands alleen voor Windows
        self.running_services   = "running_services"
        self.stopped_services   = "stopped_services"
        self.t_services         = "t_services"

    def verbindingOpzetten(self):
        try:
            functions.s.connect((self.host, self.port))
            functions.ontvangData() # ontvang bericht "voer wachtwoord in"

        # indien 't agent script niet draait of de poort niet klopt
        except ConnectionRefusedError:
            return 1

        # indien de agent niet kan worden gepingd
        except socket.timeout:
            return 2

        functions.verstuurData(self.ww) # verstuur wachtwoord
        functions.ontvangData()
        return 0

    def geefHostname(self):
        functions.verstuurData(slf.hostname)
        self.hostname = functions.ontvangData()
        return self.hostname

    def genereerHostID(self):
        # controleer of de opgegeven host al bestaat in de tabel, zo niet dan toevoegen. onthoud vervolgens 't host_id
        for rij in self.conn.execute("SELECT COUNT(*) FROM hosts WHERE naam = '" + self.hostname + "'"):
            if rij[0] != 0:
                for rij in self.conn.execute("SELECT host_id FROM hosts WHERE naam = '" + self.hostname + "'"):
                    self.host_id = rij[0]
                    return self.host_id

            else:
                self.conn.execute("INSERT INTO hosts (naam) VALUES ('" + self.hostname + "')")
                self.conn.commit()
                for rij in self.conn.execute("SELECT  last_insert_rowid() FROM hosts"):
                    self.host_id = rij[0]
                    return self.host_id

    def geefOS(self):
        functions.verstuurData(self.os)
        if self.OS == "W":
            return functions.ontvangData()[:-40]
        else:
            return functions.ontvangData()

    def geefIP(self):
        functions.verstuurData(self.ip_address)
        return functions.ontvangData()

    def geefUsers(self):
        functions.verstuurData(self.logged_on_users)
        if self.OS == "W":
            users_value = functions.ontvangData().replace("'", "") # haal onnodige quotes weg
            return users_value[1:-1] # haal blokhaken weg
        else:
            return functions.ontvangData()

    def geefDriveLabel(self):
        functions.verstuurData(self.drive_label)
        return functions.ontvangData()

    def geefFileSystem(self):
        functions.verstuurData(self.file_system)
        return functions.ontvangData()

    def geefACapacity(self):
        functions.verstuurData(self.a_capacity)
        value_s = "%.2f GB" % (functions.byteNaarGB(functions.ontvangData()))
        self.ac_value_f = float(value_s[:-3])
        return value_s

    def geefTCapacity(self):
        functions.verstuurData(self.t_capacity)
        value_s = "%.2f GB" % (functions.byteNaarGB(functions.ontvangData()))
        self.tc_value_f = float(value_s[:-3])
        return value_s

    def geefUCapacity(self):
        used_capacity = self.tc_value_f - self.ac_value_f
        naar_procent = (used_capacity / self.tc_value_f) * 100
        return float("%.2f" % naar_procent)

    def geefRunningProcesses(self):
        functions.verstuurData(self.running_processes)
        return functions.ontvangData()

    def geefCPULoad(self):
        functions.verstuurData(self.cpu_load)

        if self.OS == "W":
            # verander de komma naar een punt om er een float van te maken
            value = ""
            for i in functions.ontvangData():
                if i == ",":
                    value += "."
                else:
                    value += i

            value_s = "%.2f %%" % float(value)
            value_f = float(value_s[:-2])
            return value_s, value_f
        else:
            value = functions.ontvangData()
            return value + " %", float(value)

    def geefUptime(self):
        functions.verstuurData(self.uptime)

        if self.OS == "W":
            uptime = functions.ontvangData()

            # onnodige gegevens weghalen
            datum = uptime[0:8]
            tijd = uptime[8:-11]

            # uptime in dagen, uren niet meegerekend
            dagen = int(functions.geefDatum()) - int(datum)

            # zet notering H:M:S om naar seconden
            uren_s = int(tijd[0:2])*60*60
            minuten_s = int(tijd[2:4])*60
            seconden = int(tijd[4:6])
            totale_seconden = uren_s + minuten_s + seconden

            # uptime in seconden vandaag
            uptime_s = functions.geefTijdInSeconden() - totale_seconden

            # seconden omzetten naar procent en optellen met 't aantal dagen
            uptime_p = uptime_s/86400
            uptime_p2 = "%.2f" % uptime_p
            uptime_dagen = dagen + float(uptime_p2)
            return str(uptime_dagen) + " dagen"

        else:
            uptime_p = int(functions.ontvangData())/86400
            value = "%.2f" % uptime_p
            return value + " dagen"

    def geefAMemory(self):
        functions.verstuurData(self.a_memory)
        if self.OS == "W":
            value = functions.ontvangData()
            self.am_value = int(value)
            return str(value) + " MB"
        else:
            value = functions.byteNaarMB(functions.ontvangData())
            self.am_value = int(value)
            return str(value) + " MB"

    def geefTMemory(self):
        functions.verstuurData(self.t_memory)
        value = functions.byteNaarMB(functions.ontvangData())
        self.tm_value = int(value)
        return str(value) + " MB"

    def geefUMemory(self):
        used_memory = self.tm_value - self.am_value
        naar_procent = (used_memory / self.tm_value) * 100
        return float("%.2f" % naar_procent)

    def geefRunningServices(self):
        functions.verstuurData(self.running_services)
        return functions.ontvangData()

    def geefStoppedServices(self):
        functions.verstuurData(self.stopped_services)
        return functions.ontvangData()

    def geefTotalServices(self):
        functions.verstuurData(self.t_services)
        return functions.ontvangData()

    def verlaatSessie(self):
        functions.verstuurData(self.stop)

    def genereerGrafiek(self, grafieksoort_id, meetwaarde, tijd):
        self.grafieksoort_id = grafieksoort_id
        self.meetwaarde = meetwaarde
        self.tijd = str(tijd)

        # controleer of er voor vandaag al een grafiek is gemaakt, zo niet dan grafiek aanmaken en gegevens invoeren. anders de bestaande gebruiken
        for rij in self.conn.execute("SELECT COUNT(*) FROM grafieken WHERE datum = '" + str(self.datum) + "' AND host_id = '" + str(self.host_id) + "' AND grafieksoort_id = '" + str(self.grafieksoort_id) + "'"):

            if rij[0] != 0:
                for rij in self.conn.execute("SELECT grafiek_id FROM grafieken WHERE datum = '" + str(self.datum) + "' AND host_id = '" + str(self.host_id) + "' AND grafieksoort_id = '" + str(self.grafieksoort_id) + "'"):
                    self.grafiek_id = str(rij[0])
                    self.conn.execute("INSERT INTO meetwaarden (meetwaarde, tijd, grafiek_id) VALUES ('" + str(self.meetwaarde) + "', '" + str(self.tijd) + "', '" + self.grafiek_id + "')")
                    self.conn.commit()
                    break

            else:
                self.conn.execute("INSERT INTO grafieken (datum, grafieksoort_id, host_id) VALUES ('" + str(self.datum) + "', '" + str(self.grafieksoort_id) + "', '" + str(self.host_id) + "')")
                self.conn.commit()
                for rij in self.conn.execute("SELECT last_insert_rowid() FROM grafieken"):
                    self.grafiek_id = str(rij[0])
                    self.conn.execute("INSERT INTO meetwaarden (meetwaarde, tijd, grafiek_id) VALUES ('" + str(self.meetwaarde) + "', '" + str(self.tijd) + "', '" + self.grafiek_id + "')")
                    self.conn.commit()
                    break

        self.meetwaarden = []
        tijden = []

        for rij in self.conn.execute("SELECT meetwaarde, tijd FROM meetwaarden WHERE grafiek_id = '" + self.grafiek_id + "'"):
            self.meetwaarden.append(rij[0])
            tijden.append(rij[1])

        # genereren van grafiek
        fig = plt.figure()
        ax = fig.add_subplot(111)

        if self.grafieksoort_id == 1:
            ax.set_ylabel("Processorbelasting (%)")
            self.soort = "processorbelasting"
        elif self.grafieksoort_id == 2 and self.OS == "W":
            ax.set_ylabel("Datagebruik C: (%)")
            self.soort = "datagebruik"
        elif self.grafieksoort_id == 2 and self.OS == "L":
            ax.set_ylabel("Datagebruik /dev/sda1 (%)")
            self.soort = "datagebruik"
        elif self.grafieksoort_id == 3:
            ax.set_ylabel("Geheugengebruik (%)")
            self.soort = "geheugengebruik"

        ax.set_xlabel("Tijd",fontsize=11)
        plt.plot(tijden, self.meetwaarden, 'ro', linestyle='--', ms=4)
        plt.axis([0,24,0,100])
        xlabels = []
        for i in range(0,25):
            tijd = (str(i) + "u")
            xlabels.append(tijd)

        plt.grid(True)
        plt.yticks(np.arange(0, 101, 5))
        plt.xticks(range(0,25),xlabels,rotation=45,fontsize=9)

        # grafiek opslaan
        file = self.hostname + "_" + str(self.datum) + "_" + self.soort + '.png'
        plt.savefig(self.locatie + self.locatie_grafieken + file)

    def bewaarInCsv(self, locatie_csv):
        datum = str(self.datum)[0:4] + "-" + str(self.datum)[4:6] + "-" + str(self.datum)[6:8]
        tijd = str(functions.tijdInDecimalenNaarGewoon(self.tijd))
        datum_en_tijd = datum + " " + tijd
        pad_naar_file = self.locatie + locatie_csv

        # schrijf de column headers alleen als de file nog leeg is
        with open(pad_naar_file, 'a') as csvfile:
            fieldnames = ['datum-tijd', 'agent', 'count', 'waarde']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            with open(pad_naar_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                has_rows = False
                for line in reader:
                    has_rows = True
                if not has_rows:
                    writer.writeheader()
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': self.soort, 'waarde': self.meetwaarde})
                else:
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': self.soort, 'waarde': self.meetwaarde})

    def bewaarAlleenInCsv(self, processorbelasting, datagebruik, geheugengebruik, tijd, locatie_csv):
        datum = str(self.datum)[0:4] + "-" + str(self.datum)[4:6] + "-" + str(self.datum)[6:8]
        tijd = str(functions.tijdInDecimalenNaarGewoon(tijd))
        datum_en_tijd = datum + " " + tijd
        pad_naar_file = self.locatie + locatie_csv

        # schrijf de column headers alleen als de file nog leeg is
        with open(pad_naar_file, 'a') as csvfile:
            fieldnames = ['datum-tijd', 'agent', 'count', 'waarde']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            with open(pad_naar_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                has_rows = False
                for line in reader:
                    has_rows = True
                if not has_rows:
                    writer.writeheader()
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': "processorbelasting", 'waarde': processorbelasting})
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': "datagebruik", 'waarde': datagebruik})
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': "geheugengebruik", 'waarde': geheugengebruik})
                else:
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': "processorbelasting", 'waarde': processorbelasting})
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': "datagebruik", 'waarde': datagebruik})
                    writer.writerow({'datum-tijd': datum_en_tijd, 'agent': self.hostname, 'count': "geheugengebruik", 'waarde': geheugengebruik})

    def genereerDropdown(self):
        grafiek_items = []
        grafiek_items2 = []
        grafiek_items3 = []

        for i in range(1,4):
            # combineer de datum van de grafiek met het pad naar de grafiek en plaats dit in grafiek_items
            for rij in self.conn.execute("SELECT datum, grafieksoort_id FROM grafieken WHERE host_id = '" + str(self.host_id) + "' ORDER BY datum DESC"):
                datum_tekst = functions.datumNaarTekst(str(rij[0]))
                if rij[1] == i:
                    if i == 1:
                        path = self.locatie_grafieken + self.hostname + "_" + str(rij[0]) + "_processorbelasting.png"
                        value = (datum_tekst, path)
                        grafiek_items.append(value)
                    elif i == 2:
                        path = self.locatie_grafieken + self.hostname + "_" + str(rij[0]) + "_datagebruik.png"
                        value = (datum_tekst, path)
                        grafiek_items2.append(value)
                    elif i == 3:
                        path = self.locatie_grafieken + self.hostname + "_" + str(rij[0]) + "_geheugengebruik.png"
                        value = (datum_tekst, path)
                        grafiek_items3.append(value)

        return grafiek_items, grafiek_items2, grafiek_items3

    def geefGrafiekID(self, datum, grafieksoort_id, host_id):
        datum = functions.tekstNaarDatum(datum)
        for rij in self.conn.execute("SELECT grafiek_id FROM grafieken WHERE datum = '" + str(datum) + "' AND host_id = '" + str(host_id) + "' AND grafieksoort_id = '" + str(grafieksoort_id) + "'"):
            return str(rij[0])

functions.uploadNaarGitHub(__file__)

#sfsdfsdf
