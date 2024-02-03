# Benötigte Tools wurden zuvor in PyCharm 2023.1.2 unter "Preferences" als "Python Interpreter" für das Projekt installiert
# Tools in das Python Script importieren
import requests
from bs4 import BeautifulSoup
import pandas as pd

### Billboard Charts
# Eine Funktion definieren mit der automatisiert die Chart-Daten aus den jeweiligen Wikipedia-Seiten extrahiert werden
# Parameter y: Jahr (in zweistelligem Format: "00", "09", "14")
def webscrapingbillboard(y):
    # die Jahreszahl wird je Parameter angepasst
    URL = f"https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_20{y}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # HTML Text der auf der Website vorhandenen Tabelle (Rang, Songtitel, Künstler*innen):
    wiki_table = soup.find("table", {"class": "wikitable sortable"})
    # HTML-Tag "td" enthält das Set (Rang, Songtitel, Künstler*in) als Text

    # Listen erstellen, in die die Chartplatzierung (number), Songtitel (titles) und Künstler*innen (artists) später eingespeist werden
    list = []
    number = []
    titles = []
    artists = []

    # alle "td" Tags finden und deren Text zunächst in eine Liste zusammenführen
    titles_artists_tags = wiki_table.find_all("td")
    for td in titles_artists_tags:
        list.append(td.text)

    # list = Liste mit Platzierungen, Songtiteln, Künstler*innen

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
    with pd.ExcelWriter(
            "/Users/estern/Documents/BA_Data/Billboard_2000_2020.xlsx",
            mode="a",
            engine="openpyxl",
            if_sheet_exists="replace",
    ) as writer:
        df.to_excel(writer, sheet_name=f"20{y}")



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