# Benötigte Tools wurden zuvor in PyCharm 2023.1.2 unter "Preferences" als "Python Interpreter" für das Projekt installiert
# Tools in das Python Script importieren
import requests
from bs4 import BeautifulSoup
import regex as re
import pandas as pd

### UK Singles Chart
# Eine Funktion definieren mit der automatisiert die Chart-Daten aus den jeweiligen Wikipedia-Seiten extrahiert werden
# Parameter y: Jahr (in zweistelligem Format: "00" für das Jahr 2000, "09" für 2009, usw.)
def webscrapinguksingles(y):
    URL = f"https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_20{y}" # die Jahreszahl wird je Parameter angepasst
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # HTML Text der auf der Website vorhandenen Tabelle (Songtitel, Künstler*innen):
    wiki_table = soup.find("table", class_="wikitable sortable")
    # HTML-Tag "td" enthält das Set (verschiedene Datums- und Wochenangaben, Songtitel, Künstler*in) als Text
    # Die UK Singles Charts enthalten keine Platzierungsinformationen, da lediglich festgehalten wird wie viele Wochen ein Titel in den Top 10 war

    # Listen erstellen, in die die Songtitel (titles) und Künstler*innen (artists) später eingespeist werden
    # in number wird jedem Titel eine "künstliche Platzierung" zugeteilt, um eine Übersicht über die Anzahl der Titel zu haben und die UK Charts dem Format der Billboard Charts anzugleichen
    number = []
    titles = []
    artists = []

    # gesamten Text der Tabelle festhalten in alltext:
    alltext = wiki_table.get_text().split("\n\n")
    ind = alltext.index(f"\nSingles in 20{y}")  # Die Überschrift finden, nach der die Top Ten Singles des gesuchten Jahres aufgezählt werden (davor werden noch einige Singles aus dem Vorjahr genannt)
    l = alltext[ind + 1:]  # Die Liste auf die Singles des gesuchten Jahres reduzieren (= alles nach dem Index der Überschrift "Singles in ...")

    # Die Liste l enthält Datumsangaben (Eintritt in die Charts & "Peak") und Angaben zu den Wochen, in denen sich die Single in den Top 10 befand
    # Diese Daten werden nicht gebraucht und somit entfernt:
    li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
    lis = [x for x in li if not re.fullmatch(r"\d?", x)]
    list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]
    # 're.fullmatch' um Wochenzahlen und Datumsangaben zu entfernen
    # 're.sub' um weitere Angaben, die im Tag-Text jedes Titels erscheinen und nicht gebraucht werden, zu entfernen
    # -> z.B.: ["Rock DJ" (#5)] wird zu ["Rock DJ"]

    # list = Liste mit Songtiteln, Künstler*innen

    # Songtitel und Küntler*innen in einzelne Listen aufteilen
    i = 0
    while i < len(list):
        titles.append(list[i])
        i += 2

    i = 1
    while i < len(list):
        artists.append(list[i])
        i += 2

    # Künstliche Platzierung mit number
    i = 0
    while i < len(titles):
        number.append(i + 1)
        i += 1

    # mit der pandas library ein Dataframe erstellen mit den Spalten "Nummer", "Songtitel", "Künstler*innen"
    data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
    df = pd.DataFrame(data)

    # Dataframe als eigenes Worksheet in .xlsx Dokument speichern
    with pd.ExcelWriter(
            "/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx",
            mode="a",
            engine="openpyxl",
            if_sheet_exists="replace",
    ) as writer:
        df.to_excel(writer, sheet_name=f"20{y}")


