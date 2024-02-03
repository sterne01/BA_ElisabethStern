from BA_func_ws_bill import *

# Das .xlsx-Dokument mit dem Jahr 2000 beginnend erstellen

### 2000 ###

# Das Jahr 2000 wird einzeln behandelt, da mit der Funktion "webscrapingbillboard" ein Fehler auftritt
# Gewünschte Website als URL-Variable speichern, mit "requests" library anfragen und mit BeautifulSoup den Inhalt der Website einlesen
URL = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2000"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# Auf der Website vorhandene Tabelle mit (Rang, Songtitel, Künstler*innen) finden
wiki_table = soup.find("table")
# Man kann erkennen, dass der HTML-Tag "td" jeweils ein Set von Rang, Songtitel, Künstler*in enthält

# Listen erstellen, in die die Chart-Platzierung (number), Songtitel (titles) und Künstler*innen (artists) später eingespeist werden
list = []
number = []
titles = []
artists = []

# alle "td" Tags finden und deren Text zunächst in eine Liste zusammenführen
titles_artists_tags = wiki_table.find_all("td")
for td in titles_artists_tags:
    list.append(td.text)

# Fehler ist, dass bei einem Song der Name des Künstlers nicht angegeben ist, da zwei aufeinanderfolgende Songs vom selben Künstler stammen
# Nach Abgleich mit der Wikipedia Seite, Einfügen des Künstlers an der korrekten Stelle in der Gesamtliste
i = list.index("24")
list.insert(i, "Marc Anthony\n")
# list = Platzierungen, Songtitel, Künstler*innen

# Die Ränge, Songtitel und Küntler*innen in einzelne Listen aufteilen
i = 0
while i < len(list):
    number.append(list[i])
    i += 3

i = 1
while i < len(list):
    titles.append(list[i])
    i += 3

i = 2
while i < len(list):
    artists.append(list[i])
    i += 3

# mit der pandas library ein Dataframe erstellen mit den Spalten "Nummer", "Songtitel", "Künstler*innen"
data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

# Dataframe in ein .xlsx Dokument umwandeln und lokal speichern
df.to_excel("/Users/estern/Documents/BA_Data/Billboard_2000_2020.xlsx", sheet_name="2000")
print("00 erfolgreich heruntergeladen")


### 2001-2007 ###
# Die herunterzuladenden Jahre in einer Liste speichern
years = ["01", "02", "03", "04", "05", "06", "07"]

# Durch years iterieren
for y in years:
    webscrapingbillboard(y)
    print(y+" erfolgreich heruntergeladen")


### 2008 ###
# für Jahr 2008 tritt derselbe Fehler (ab jetzt "Fehler SKIP" genannt) auf wie im Jahr 2000, daher Einzeldurchlauf:
URL = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2008"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table")

list = []
number = []
titles = []
artists = []

titles_artists_tags = wiki_table.find_all("td")
for td in titles_artists_tags:
    list.append(td.text)

i = list.index("11")
list.insert(i, "Chris Brown\n")
j = list.index("18")
list.insert(j, "Rihanna\n")

i = 0
while i < len(list):
    number.append(list[i])
    i += 3

i = 1
while i < len(list):
    titles.append(list[i])
    i += 3

i = 2
while i < len(list):
    artists.append(list[i])
    i += 3

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/Billboard_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2008")

print("08 erfolgreich heruntergeladen")

### 2009-2011 ###
moreyears = ["09", "10", "11"]
# Durch moreyears iterieren
for y in moreyears:
    webscrapingbillboard(y)
    print(y+" erfolgreich heruntergeladen")


### 2012 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2012"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", {"class": "wikitable sortable"})

list = []
number = []
titles = []
artists = []

titles_artists_tags = wiki_table.find_all("td")
for td in titles_artists_tags:
    list.append(td.text)

i = list.index("18")
list.insert(i, "Flo Rida")

i = 0
while i < len(list):
    number.append(list[i])
    i += 3

i = 1
while i < len(list):
    titles.append(list[i])
    i += 3

i = 2
while i < len(list):
    artists.append(list[i])
    i += 3

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/Billboard_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2012")

print("12 erfolgreich heruntergeladen")

### 2013 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2013"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", {"class": "wikitable sortable"})

list = []
number = []
titles = []
artists = []

titles_artists_tags = wiki_table.find_all("td")
for td in titles_artists_tags:
    list.append(td.text)

i = list.index("19")
list.insert(i, "Miley Cyrus")

i = 0
while i < len(list):
    number.append(list[i])
    i += 3

i = 1
while i < len(list):
    titles.append(list[i])
    i += 3

i = 2
while i < len(list):
    artists.append(list[i])
    i += 3

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/Billboard_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2013")

print("13 erfolgreich heruntergeladen")

### 2014 ###
webscrapingbillboard("14")
print("14 erfolgreich heruntergeladen")

### 2015 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2015"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", {"class": "wikitable sortable"})

list = []
number = []
titles = []
artists = []

titles_artists_tags = wiki_table.find_all("td")
for td in titles_artists_tags:
    list.append(td.text)

i = list.index("11")
list.insert(i, "The Weeknd")

i = 0
while i < len(list):
    number.append(list[i])
    i += 3

i = 1
while i < len(list):
    titles.append(list[i])
    i += 3

i = 2
while i < len(list):
    artists.append(list[i])
    i += 3

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/Billboard_2000_2020.xlsx",
          mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2015")

print("15 erfolgreich heruntergeladen")

### 2016 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2016"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", {"class": "wikitable sortable"})

list = []
number = []
titles = []
artists = []

titles_artists_tags = wiki_table.find_all("td")
for td in titles_artists_tags:
    list.append(td.text)

i = list.index("3")
list.insert(i, "Justin Bieber")
j = list.index("22")
list.insert(j, "Twenty One Pilots")

i = 0
while i < len(list):
    number.append(list[i])
    i += 3

i = 1
while i < len(list):
    titles.append(list[i])
    i += 3

i = 2
while i < len(list):
    artists.append(list[i])
    i += 3

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/Billboard_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2016")

print("16 erfolgreich heruntergeladen")

### 2017-2020 ###
evenmoreyears = ["17", "18", "19", "20"]
# Durch evenmoreyears iterieren
for y in evenmoreyears:
    webscrapingbillboard(y)
    print(y+" erfolgreich heruntergeladen")
