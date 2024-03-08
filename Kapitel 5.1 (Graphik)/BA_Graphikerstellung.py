from matplotlib import pyplot as plt

### UK Singles Charts ###
labels = ["female", "male", "Kollaborationen",  "genderfluid, male organism, non-binary"]
# absolute Häufigkeiten der Geschlechter in den Songtexten von Solokünstler*innen und Kollaborationen
sizes = [569, 649, 616, 18]
# die Keile des Kreisdiagramms mit explode leicht auseinanderzerren (weiße Zwischenräume entstehen lassen
# für Übersichtlichkeit)
explode = [0.01, 0.01, 0.01, 0.01]

colors = "red", "blue", "violet", "yellow"

plt.figure(figsize=(7,7))
# mit autopct ebenfalls die Prozentzahlen aller Keile einfügen
plt.pie(sizes, colors=colors, explode=explode, autopct='%1.1f%%', pctdistance = 1.2)
# Legende mit den Geschlechtern einfügen
plt.legend(labels, loc="upper left", prop={"size":"medium", "family":"monospace"}, framealpha=0.8)
plt.title(label="Solokünstler*innen & Kollaborationen der UK Singles Charts (2000-2020)")
# Graphik speichern
plt.savefig('UKS_Dv.png', dpi=300)
plt.show()


### Billboard ###
# gleiches Vorgehen wie oben #
labels = ["female", "male", "Kollaborationen",  "genderfluid, transwoman, non-binary"]
sizes = [422, 586, 595, 25]
explode = [0.01, 0.01, 0.01, 0.01]

colors = "red", "blue", "violet", "yellow"

plt.figure(figsize=(7,7))
plt.pie(sizes, colors=colors, explode=explode, autopct='%1.1f%%', pctdistance = 1.2)
plt.legend(labels, loc="upper left", prop={"size":"medium", "family":"monospace"}, framealpha=0.8)
plt.title(label="Solokünstler*innen & Kollaborationen der Billboard Charts (2000-2020)")
plt.savefig('BillB_Dv.png', dpi=300)
plt.show()
