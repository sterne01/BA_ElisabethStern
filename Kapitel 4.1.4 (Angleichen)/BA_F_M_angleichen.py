import pandas as pd
#
# Mit diesem Programm wird die Anzahl der Künstler und Künstlerinnen aneinander angepasst, sodass in jedem Jahr gleich
# viele Songs von Frauen und Männern enthalten sind.
# Dafür wurden im vorhinein die Excel-Worksheets alphabetisch nach der Spalte "sex or gender" sortiert. Also werden in
# jedem Worksheet zunächst alle Frauen ("female") und danach alle Männer ("male") aufgezählt.
# Jegliche andere Geschlechter ("non-binary", "genderfluid", etc.) wurden nicht miteinbezogen.

# Alle Titel der einzelnen Worksheets als Variablen speichern, damit durch sie iteriert werden kann (2000 wird je
# einzeln behandelt, um das Excel Dokument zu erstellen):
all_ws = ["2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010",
         "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]

### Billboard 2000 - 2020 ###
# Dateipfad als Variable speichern
x_path = "/Users/estern/Documents/BA_Data/FinalORBillboard2000_2020.xlsx"

### 2000 ###
# Excel Sheet einlesen und die letzten zwei Zeilen mit weiblichem Interpret überspringen, da das Jahr 2000 ausnahmsweise
# mehr Frauen als Männer enthält. So wird die Anzahl aneinander angepasst.
x_file = pd.read_excel(x_path, "2000", skiprows=[30, 31])
# Überprüfen, ob nun die Anzahl der Männer und Frauen gleich ist.
print("Summe gleich?", "2000", (sum(x_file["sex or gender"]=="male") == sum(x_file["sex or gender"]=="female")))
# ein neues Excel Dokument namens "BillB_gekürzt" anlegen und das Jahr 2000 in ein Worksheet mit dem Namen 2000 einfügen:
x_file.to_excel("/Users/estern/Documents/BA_Data/BillB_gekürzt.xlsx", sheet_name="2000")

### Restliche Jahre ###
# durch alle Worksheets iterieren:
for y in all_ws:
    x_file = pd.read_excel(x_path, f"{y}")
    if (sum(x_file["sex or gender"] == "female")) < (sum(x_file["sex or gender"] == "male")):
        # die Summe der Frauen als Variable "end" anlegen
        end = (sum(x_file["sex or gender"] == "female"))
        # aus dem Worksheet nur so viele Zeilen entnehmen (und in "part" speichern"), dass insgesamt genau doppelt so
        # viele Zeilen wie Zeilen mit weiblichen Interpreten existieren (und so die erste Hälfte der Zeilen des Worksheets
        # aus Frauen besteht und die zweite aus Männern)
        part = x_file[0:(end*2)]
        print("Summe gleich?",y, (sum(part["sex or gender"] == "male") == sum(part["sex or gender"] == "female")))
        # dem Excel Dokument "BillB_gekürzt" hinzufügen, den Namen des Worksheet jeweils an das akutelle Jahr anpassen (y)
        with pd.ExcelWriter(
                "/Users/estern/Documents/BA_Data/BillB_gekürzt.xlsx",
                mode="a",
                engine="openpyxl",
                if_sheet_exists="replace",
        ) as writer:
            part.to_excel(writer, sheet_name=f"{y}")
    else:
        print("Ausnahme", y)


### UK Singles ###

### 2000 ###
# Ausnahme 2000: Männer und Frauen sind schon ausgeglichen
x_path2 = "/Users/estern/Documents/BA_Data/FinalORUKSin_2000_2020.xlsx"
x_file = pd.read_excel(x_path2, "2000")
print("Summe gleich?","2000", (sum(x_file["sex or gender"] == "male") == sum(x_file["sex or gender"] == "female")))
# ein neues Excel Dokument namens "UKS_gekürzt" anlegen und das Jahr 2000 in ein Worksheet mit dem Namen 2000 einfügen:
x_file.to_excel("/Users/estern/Documents/BA_Data/UKS_gekürzt.xlsx", sheet_name="2000")

### 2001 ###
# Ausnahme 2001: mehr Frauen als Männer
x_file = pd.read_excel(x_path2, "2001", skiprows=[38, 39, 40, 41, 42, 43])
print("Summe gleich?", "2001", sum(x_file["sex or gender"] == "male") == sum(x_file["sex or gender"] == "female"))
with pd.ExcelWriter(
        "/Users/estern/Documents/BA_Data/UKS_gekürzt.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
) as writer:
    x_file.to_excel(writer, sheet_name="2001")


### Restliche Jahre ###
# durch alle Worksheets iterieren:
# Vorgehen s.o.
for y in all_ws:
    x_file = pd.read_excel(x_path2, f"{y}")
    if (sum(x_file["sex or gender"] == "female"))<(sum(x_file["sex or gender"] == "male")):
        end = (sum(x_file["sex or gender"] == "female"))
        part = x_file[0:(end*2)]
        print("Summe gleich?",y, (sum(part["sex or gender"] == "male") == sum(part["sex or gender"] == "female")))
        # dem Excel Dokument "UKS_gekürzt" hinzufügen, den Namen des Worksheet jeweils an das akutelle Jahr anpassen (y)
        with pd.ExcelWriter(
                "/Users/estern/Documents/BA_Data/UKS_gekürzt.xlsx",
                mode="a",
                engine="openpyxl",
                if_sheet_exists="replace",
        ) as writer:
            part.to_excel(writer, sheet_name=f"{y}")
    # falls die Summe der Frauen und Männer gleich ist, das Worksheet unverändert "UKS_gekürzt" hinzufügen
    elif (sum(x_file["sex or gender"] == "female")) == (sum(x_file["sex or gender"] == "male")):
        with pd.ExcelWriter(
                "/Users/estern/Documents/BA_Data/UKS_gekürzt.xlsx",
                mode="a",
                engine="openpyxl",
                if_sheet_exists="replace",
        ) as writer:
            x_file.to_excel(writer, sheet_name=f"{y}")
        print(y, "hinzugefügt")
    else:
        print("Ausnahme", y)