import pandas as pd
import lyricsgenius as lg
import regex as re


# Alle Pfade zu benötigten existierenden Dateien und neu zu schreibenden Dateien in Variablen festhalten
path_bill = "/Users/estern/Documents/BA_Data/F_M_Ausgeglichen/BillB_gekürzt.xlsx"
path_f_lyr = "/Users/estern/Documents/BA_Data/F_Bill_Lyr/"
path_m_lyr = "/Users/estern/Documents/BA_Data/M_Bill_Lyr/"

genius = lg.Genius("ZI8bJmhp-URBvInIRXIEN1tkR0trUmb-3acnZgZcOlqUaPG3XEBVbUrg9BtfLA5F", skip_non_songs=True,
                   remove_section_headers=True, timeout=15, sleep_time=0.5, retries=3)

# Funktion "get_lyrics" wurde aus den Codes "BA_Lyrics_Bill" und "BA_Lyrics_UKS" genommen und abgeändert, um erneut
# nach fehlerhaften Songtexten zu suchen
def get_lyrics(path, yearstr, line):
    lyrics = []
    x_file = pd.read_excel(path, yearstr)
    # Die unten angegebene Zeile ("line") mit dem fehlerhaften Songtext als Variable speichern
    pos = x_file.loc[x_file["Unnamed: 0"] == line]
    # Drucken, welcher Song es ist und welche Künstler*innen angegeben sind
    print(pos["Songtitel"].values[0], pos["K_all"].values[0])
    # Den Titel und Künstler*innen in Variablen speichern
    t = pos["Songtitel"].values[0]
    a = pos["K1"].values[0]
    # den Song mit Genius API anfragen und lyrics der Liste "lyrics" hinzufügen
    # dabei wurde die Suche mit verschiedenen Varianten des Titels oder der Künstler*innen probiert,
    # z.B. wird zuerst bei "artist" "Lauv featuring Troye Sivan" eingegeben, wenn dies kein Ergebnis liefert mit
    # "Lauv, Troye Sivan" probieren, usw.
    song = genius.search_song(title=t, artist=a)
    lyrics.append(song.lyrics)
    # Nicht benötigte Informationen aus allen Songtexten entfernen
    lyrics_final = [re.sub(pattern=r'(\d+)?Embed|(\d+)?\sContributors(Translation.+)?(.+Lyrics)?', string=x, repl='')
                    for x in lyrics]
    # die gefundenen Lyrics ausgeben
    return lyrics_final[0]

# Das Jahr und die Zeile des fehlerhaften Songtextes eingeben
year = "2000"
line = 26
# Das Resultat der erneuten Suche des Songtextes mit "get_lyrics" ausgeben
result = get_lyrics(path_bill, year, line)
print(result)

# Die Zeile, die ausgebessert wird, als Variable speichern
x_file = pd.read_excel(path_bill, year)
pos = x_file.loc[x_file["Unnamed: 0"]==line]

# je nach Geschlecht eine neue .txt Datei mit dem verbesserten Songtext erstellen
gender = pos["sex or gender"]
if gender[line] == "female":
    with open(path_f_lyr + f'{year}_' + f'{line}' + '.txt', 'w+') as f:
        f.write(result)
elif gender[line] == "male":
    with open(path_m_lyr + f'{year}_' + f'{line}' + '.txt', 'w+') as f:
        f.write(result)