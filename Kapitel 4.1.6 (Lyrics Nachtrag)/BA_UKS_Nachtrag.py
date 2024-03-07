import pandas as pd
import lyricsgenius as lg
import regex as re

### Annotationen zu diesem Code s. "BA_Bill_Nachtrag" ###


# Alle Pfade zu benötigten existierenden Dateien und neu zu schreibenden Dateien in Variablen festhalten
path_uks = "/Users/estern/Documents/BA_Data/F_M_Ausgeglichen/UKS_gekürzt.xlsx"
path_f_lyr = "/Users/estern/Documents/BA_Data/F_UKS_Lyr/"
path_m_lyr = "/Users/estern/Documents/BA_Data/M_UKS_Lyr/"


genius = lg.Genius("ZI8bJmhp-URBvInIRXIEN1tkR0trUmb-3acnZgZcOlqUaPG3XEBVbUrg9BtfLA5F", skip_non_songs=True,
                   remove_section_headers=True, timeout=15, sleep_time=0.5, retries=3)


def get_lyrics(path, yearstr, line):
    lyrics = []
    x_file = pd.read_excel(path, yearstr)
    pos = x_file.loc[x_file["Unnamed: 0"] == line]
    print(pos["Songtitel"].values[0], pos["K_all"].values[0])
    t = pos["Songtitel"].values[0]
    a = pos["K1"].values[0]
    song = genius.search_song(title=t, artist=a)
    lyrics.append(song.lyrics)
    lyrics_final = [re.sub(pattern=r'(\d+)?Embed|(\d+)?\sContributors(Translation.+)?(.+Lyrics)?', string=x, repl='')
                    for x in lyrics]
    return lyrics_final[0]

year = "2002"
line = 68
result = get_lyrics(path_uks, year, line)
print(result)


x_file = pd.read_excel(path_uks, year)
pos = x_file.loc[x_file["Unnamed: 0"]==line]

gender = pos["sex or gender"]
if gender[line] == "female":
    with open(path_f_lyr + f'{year}_' + f'{line}' + '.txt', 'w+') as f:
        f.write(result)
elif gender[line] == "male":
    with open(path_m_lyr + f'{year}_' + f'{line}' + '.txt', 'w+') as f:
        f.write(result)