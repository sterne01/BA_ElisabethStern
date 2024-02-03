from BA_func_ws_uks import *

# Das .xlsx-Dokument mit dem Jahr 2000 beginnend erstellen

### 2000 ###
URL = "https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_2000"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# HTML Text der auf der Website vorhandenen Tabelle (Songtitel, Künstler*innen):
wiki_table = soup.find("table", class_="wikitable sortable")
# HTML-Tag "td" enthält das Set (verschiedene Datums- und Wochenangaben, Songtitel, Künstler*in) als Text
# Die UK Singles Charts enthalten keine Platzierungsinformationen, da lediglich festgehalten wird wie viele Wochen ein Titel in den Top 10 war
#print(wiki_table)
# Listen erstellen, in die die Songtitel (titles) und Künstler*innen (artists) später eingespeist werden
# in number wird jedem Titel eine "künstliche Platzierung" zugeteilt, um eine Übersicht über die Anzahl der Titel zu haben und die UK Charts dem Format der Billboard Charts anzugleichen
number = []
titles = []
artists = []

# gesamten Text der Tabelle festhalten in alltext:
alltext = wiki_table.get_text().split("\n\n")
ind = alltext.index("\nSingles in 2000") # Die Überschrift finden, nach der die Top Ten Singles des gesuchten Jahres aufgezählt werden (davor werden noch einige Singles aus dem Vorjahr genannt)
l = alltext[ind+1:] # Die Liste auf die Singles des gesuchten Jahres reduzieren (= alles nach dem Index der Überschrift "Singles in ...")

# Die Liste l enthält Datumsangaben (Eintritt in die Charts & "Peak") und Angaben zu den Wochen, in denen sich die Single in den Top 10 befand
# Diese Daten werden nicht gebraucht und somit entfernt:
li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
lis = [x for x in li if not re.fullmatch(r"\d", x)]
list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]
# 're.fullmatch' um Wochenzahlen und Datumsangaben zu entfernen
# 're.sub' um weitere Angaben, die im Tag-Text jedes Titels erscheinen und nicht gebraucht werden, zu entfernen
# -> z.B.: ["Rock DJ" (#5)] wird zu ["Rock DJ"]

# list = Liste mit allen Songtiteln, Künstler*innen

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
    number.append(i+1)
    i += 1

# mit der pandas library ein Dataframe erstellen mit den Spalten "Nummer", "Songtitel", "Künstler*innen"
data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

# Dataframe in ein .xlsx Dokument schreiben im Worksheet "2000"
df.to_excel("/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx", sheet_name="2000")
print("00 erfolgreich heruntergeladen")


### 2001 ###
# S. BA_billboardfinal.py: Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_2001"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", class_="wikitable sortable")
number = []
titles = []
artists = []

alltext = wiki_table.get_text().split("\n\n")
ind = alltext.index("\nSingles in 2001")
l = alltext[ind+1:]

li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
lis = [x for x in li if not re.fullmatch(r"\d", x)]
list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]

# Einfügen des/r fehlenden Künstlers/in
i = list.index('"Uptown Girl"')
list.insert(i, "Manic Street Preachers")

i = 0
while i < len(list):
    titles.append(list[i])
    i += 2

i = 1
while i < len(list):
    artists.append(list[i])
    i += 2

i = 0
while i < len(titles):
    number.append(i+1)
    i += 1

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2001")

print("01 erfolgreich heruntergeladen")


### 2002 - 2008 ###
years = ["02", "03", "04", "05", "06", "07", "08"]

for y in years:
    webscrapinguksingles(y)
    print(y+" erfolgreich heruntergeladen")


### 2009 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_2009"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", class_="wikitable sortable")

number = []
titles = []
artists = []

alltext9 = wiki_table.get_text().split("\n\n")
ind = alltext9.index("\nSingles in 2009")
l = alltext9[ind+1:]

li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
lis = [x for x in li if not re.fullmatch(r"\d", x)]
list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]

i = list.index('"Diamond Rings"')
list.insert(i, "Michael Jackson")

i = 0
while i < len(list):
    titles.append(list[i])
    i += 2

i = 1
while i < len(list):
    artists.append(list[i])
    i += 2

i = 0
while i < len(titles):
    number.append(i+1)
    i += 1

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2009")

print("09 erfolgreich heruntergeladen")


### 2010 - 2016 ###
moreyears = ["10", "11", "12", "13", "14", "15", "16"]

for y in moreyears:
    webscrapinguksingles(y)
    print(y+" erfolgreich heruntergeladen")


### 2017 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_2017"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", class_="wikitable sortable")

number = []
titles = []
artists = []

alltext17 = wiki_table.get_text().split("\n\n")
ind = alltext17.index("\nSingles in 2017")
l = alltext17[ind+1:]

li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
lis = [x for x in li if not re.fullmatch(r"\d", x)]
list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]

i = list.index('"September Song"')
list.insert(i, "Ed Sheeran")

k = list.index('"New Man"')
o = 0
while o < 6:
    list.insert(k, "Ed Sheeran")
    k += 2
    o += 1

i = list.index('"Sorry Not Sorry"')
list.insert(i, "Taylor Swift")

i = 0
while i < len(list):
    titles.append(list[i])
    i += 2

i = 1
while i < len(list):
    artists.append(list[i])
    i += 2

i = 0
while i < len(titles):
    number.append(i+1)
    i += 1

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2017")

print("17 erfolgreich heruntergeladen")

### 2018 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_2018"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", class_="wikitable sortable")

number = []
titles = []
artists = []

alltext18 = wiki_table.get_text().split("\n\n")
ind = alltext18.index("\nSingles in 2018")
l = alltext18[ind+1:]

li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
lis = [x for x in li if not re.fullmatch(r"\d", x)]
list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]

i = list.index('"Girls Like You"')
list.insert(i, "Drake")

i = 0
while i < len(list):
    titles.append(list[i])
    i += 2

i = 1
while i < len(list):
    artists.append(list[i])
    i += 2

i = 0
while i < len(titles):
    number.append(i+1)
    i += 1

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2018")

print("18 erfolgreich heruntergeladen")


### 2019 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_2019"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", class_="wikitable sortable")

number = []
titles = []
artists = []

alltext19 = wiki_table.get_text().split("\n\n")
ind = alltext19.index("\nSingles in 2019")
l = alltext19[ind+1:]

li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
lis = [x for x in li if not re.fullmatch(r"\d?", x)]
list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]

i = list.index('"Options"')
list.insert(i, "Ariana Grande")

i = 0
while i < len(list):
    titles.append(list[i])
    i += 2

i = 1
while i < len(list):
    artists.append(list[i])
    i += 2

i = 0
while i < len(titles):
    number.append(i+1)
    i += 1

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2019")

print("19 erfolgreich heruntergeladen")


### 2020 ###
# Fehler SKIP:
URL = "https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_2020"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

wiki_table = soup.find("table", class_="wikitable sortable")

number = []
titles = []
artists = []

alltext20 = wiki_table.get_text().split("\n\n")
ind = alltext20.index("\nSingles in 2020")
l = alltext20[ind+1:]

li = [re.sub(pattern=r'"\s.+', string=x.rstrip(), repl='"') for x in l if not re.fullmatch(r'\n?\d{1,2}', x)]
lis = [x for x in li if not re.fullmatch(r"\d?", x)]
list = [x for x in lis if not re.fullmatch(r'\n?\d{1,2}\s\w+\s\d{4}', x)]

i = list.index('"Break Up Song"')
list.insert(i, "Dua Lipa")

i = 0
while i < len(list):
    titles.append(list[i])
    i += 2

i = 1
while i < len(list):
    artists.append(list[i])
    i += 2

i = 0
while i < len(titles):
    number.append(i+1)
    i += 1

data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists}
df = pd.DataFrame(data)

with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/UKSingles_2000_2020.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    df.to_excel(writer, sheet_name="2020")

print("20 erfolgreich heruntergeladen")

