# Benötigte Tools wurden zuvor in PyCharm 2023.1.2 unter "Preferences" als "Python Interpreter" für das Projekt installiert
# Tools in das Python Script importieren

from requests.exceptions import Timeout
import pandas as pd
import lyricsgenius as lg
import regex as re

# Alle Pfade zu benötigten existierenden Dateien und neu zu schreibenden Dateien in Variablen festhalten
path_uks = "/Users/estern/Documents/BA_Data/F_M_Ausgeglichen/UKS_gekürzt.xlsx"
new_lyric_file = "/Users/estern/Documents/BA_Data/UKS+Lyrics.xlsx"
path_f_lyr = "/Users/estern/Documents/BA_Data/F_UKS_Lyr/"
path_m_lyr = "/Users/estern/Documents/BA_Data/M_UKS_Lyr/"
path_NaN = "/Users/estern/Documents/BA_Data/NaN_UKS/"

# Alle Jahre bis auf 2000 (wird einzeln behandelt) als Liste festhalten
all_ws = ["2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009",
          "2010", "2011", "2012", "2013","2014", "2015", "2016", "2017", "2018", "2019", "2020"]

# Die Instanz "genius" definieren, in der mit dem "Access Token" Zugang zu Genius angefragt wird. Weitere Parameter:
# "remove_section_headers": Überschriften, wie "Chorus", "Verse 1" entfernen; "timeout" usw.: Angaben wie lange und
# oft nach einem Songtext gesucht werden soll
genius = lg.Genius("ZI8bJmhp-URBvInIRXIEN1tkR0trUmb-3acnZgZcOlqUaPG3XEBVbUrg9BtfLA5F", skip_non_songs=True,
                   remove_section_headers=True, timeout=15, sleep_time=0.5, retries=3)

# Funktion um alle Lyrics zu jedem Jahr herunterzuladen, Parameter: "path": Pfad zur Excel Datei mit den Songtiteln &
# Künstler*innen, "yearstr": Jahr
def get_lyrics(path, yearstr):
    lyrics = []
    x_file = pd.read_excel(path, yearstr)
    # Länge der Spalte ausgeben, damit am Ende überprüft werden kann ob alle Songtexte heruntergeladen wurden
    print(len(x_file["Songtitel"]))
    i = 1 # 1, damit Header übersprungen wird
    # durch alle Titel und Künstler*innen iterieren
    for t, a in zip(x_file["Songtitel"],x_file["K_all"]):
        # jeweils den Song mit Genius API anfragen und falls (if) es ein Ergebnis gibt -> lyrics der Liste "lyrics"
        # hinzufügen (lyrics.append(song.lyrics)
        try:
            song = genius.search_song(title=t, artist=a)
        except Timeout as e:
            continue
        if song is not None:
            lyrics.append(song.lyrics)
            print(i)
            i += 1
        else:
            # falls keine Lyrics gefunden werden -> Datei mit Wort "empty" erstellen
            lyrics.append("empty")
            i += 1
    # Nicht benötigte Informationen aus allen Songtexten entfernen
    lyrics_final = [re.sub(pattern=r'(\d+)?Embed|(\d+)?\sContributors(Translations.+)?(.+Lyrics)?', string=x, repl='')
                    for x in lyrics]
    print(yearstr, "komplett heruntergeladen")
    # die Liste aller Lyrics ausgeben
    return lyrics_final

### 2000 ###
# Jahr 2000 wird einzeln behandelt und damit eine neue Excel Datei geschrieben
lyr2000 = get_lyrics(path_uks, "2000")

ly_df = pd.DataFrame({"Lyrics": pd.Series(lyr2000)})
og_df = pd.read_excel(path_uks, "2000")

print(len(lyr2000))
print(len(og_df))
# Der originalen Excel Datei, die in path_bill hinterlegt, eine neue Spalte mit allen Songtexten hinzufügen und in einer
# neuen Excel Datei speichern
complete = pd.concat([og_df, ly_df], axis=1)
complete.to_excel(new_lyric_file, sheet_name="2000")

## alle Lyrics nun in einzelnen .txt Dateien speichern

new = pd.read_excel(new_lyric_file, "2000")

# dafür durch alle Zeilen der "Lyrics" Spalte gehen...
i = 0
gender = new["sex or gender"]
for x in new["Lyrics"]:
    # und je nachdem, ob der/die Künstler/in weiblich oder männlich ist, in den dafür angelegten Ordnern speichern
    # Benennen nach dem Format "2000_"+Zähler "i" (Nummer der Reihe)
    if gender[i] == "female":
        with open(path_f_lyr+'2000_'+f'{i}'+'.txt', 'w') as f:
            f.write(x)
            i += 1
    elif gender[i] == "male":
        with open(path_m_lyr+'2000_'+f'{i}'+'.txt', 'w') as f:
            f.write(x)
            i += 1

# Nun durch alle restlichen Jahre/Worksheets in der Billboard Excel Datei iterieren und nach dem gleichen Prinzip wie
# im Jahr 2000 jeweils eine neue Spalte mit "Lyrics" hinzufügen, der neuen Excel Datei als Worksheet hinzufügen
# und im Anschluss jeden Songtext in eine .txt Datei schreiben.
for y in all_ws:
    ly = get_lyrics(path_uks, y)
    ly_df = pd.DataFrame({"Lyrics": pd.Series(ly)})
    og_df = pd.read_excel(path_uks, y)
    comp = pd.concat([og_df, ly_df], axis=1)

    with pd.ExcelWriter(
            new_lyric_file,
            mode="a",
            engine="openpyxl",
            if_sheet_exists="replace",
    ) as writer:
        comp.to_excel(writer, sheet_name=y)

    new = pd.read_excel(new_lyric_file, y)

    i = 0
    gender = new["sex or gender"]
    for x in new["Lyrics"]:
        # falls lyricsgenius keinen Songtext findet (also "empty" in der Lyricsliste steht (s.o. "get_lyrics" Funktion)),
        # wird die Datei einem eigenen Ordner mit leeren Dateien hinzugefügt, sodass diese im Nachhinein noch einmal
        # ausgebessert werden können
        if x == "empty":
            with open(path_NaN + y + f'_{i}' + '.txt', 'w') as f:
                f.write(x)
                i += 1
        elif gender[i] == "female":
            with open(path_f_lyr + y + f'_{i}' + '.txt', 'w') as f:
                f.write(x)
                i += 1
        elif gender[i] == "male":
            with open(path_m_lyr + y + f'_{i}' + '.txt', 'w') as f:
                f.write(x)
                i += 1
