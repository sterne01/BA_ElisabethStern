# Für das POS-Tagging & Lemmatisieren
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import glob
# Für das Topic Modelling:
import little_mallet_wrapper as m

### TEXT PREPROCESSING ###
# Stoppwörter der nltk Bibliothek herunterladen
nltk.download("stopwords")

# Pfad zum Ordner der Songtext Dokumente
path = "/Users/estern/Documents/BA_Data/M_UKS_Lyr/"

lyricsstrings = []

# Alle Dokumente des Ordners mit den Lyrics auflisten und prüfen, ob die Länge mit den von glob gefundenen
# Dateien übereinstimmt, also ob alle Dateien im Ordner gelesen werden können
print("Anzahl der Lyricsdokumente: ",len(glob.glob(path+"*")))

# Durch alle Lyricsdokumente iterieren und sie "lyricsstrings" hinzufügen
for file in sorted(glob.glob(path+"*")):
    with open(file, 'r') as f:
        data = f.read()
        lyricsstrings.append(str(data))

lemma = WordNetLemmatizer()

# Alle Wörter der Songtexte lemmatisieren (dafür die einzelnen Lyrics-Strings tokenisieren) und wieder zu einem String
# zusammenfügen
lemmatized = []
for string in lyricsstrings:
    l = ""
    for word in word_tokenize(string):
        l += str(lemma.lemmatize(word)) + " "

    lemmatized.append(l)

# Den lemmatisierten String tokenisieren, in Kleinbuchstaben umwandeln und POS-Tags hinzufügen
tokenized = []
for word in lemmatized:
    tokenized.append(nltk.pos_tag(word_tokenize(word.lower()),
                                  tagset="universal"))

# Für das Topic Modelling nur NOUNs und ADJectives behalten -> Wörter mit aussagekräftigem Inhalt
# Diese in "topicslist" speichern
topicslist = []
for song in tokenized:
    newstring = ""
    for taggedword in song:
        if taggedword[1] == "NOUN":
            newstring += taggedword[0] + " "
        elif taggedword[1] == "ADJ":
            newstring += taggedword[0] + " "

    topicslist.append(newstring)

# print("Nouns and Adjectives for Topic Modelling:", topicslist) # kann hier ausgegeben werden, falls eine Übersicht erwünscht ist


### TOPIC MODELLING ###
# Pfad zu Mallet und zum Speicherort als Variablen speichern
path_mallet = "/Applications/mallet-2.0.8/bin/mallet"
path_output = "/Users/estern/Documents/BA_Data/Mallet_Daten/M_UKS"

# Die bearbeiteten Songtexte in der "topicslist" weiter für den Trainingsprozess vorbereiten
# (Stoppwörter entfernen, Satzzeichen entfernen)
# "english Kopie" ist die personalisierte Stoppwortliste für das Lyricskorpus. Vollständige Liste auf github.
training_data = topicslist
training_data = [m.process_string(t, stop_words=stopwords.words("english Kopie"), remove_punctuation=True)
                 for t in training_data]

# Anfang der Trainingsdaten anzeigen, falls erwünscht
# print(training_data[0])

# Ein Topic Modell auf die Songtexte trainieren
# Dieses als Variablen "Topic Keys" und "Topic Distributions" speichern
# Anzahl gewünschter Topics festlegen ("num_topics")
topic_keys, topic_distributions = m.quick_train_topic_model(path_to_mallet=path_mallet,
                                                            output_directory_path=path_output, num_topics=8,
                                                            training_data=training_data)


# Pfade zu Mallet Files (Topic Keys, Topic Distribution, Word Weights)
tk = "/Users/estern/Documents/BA_Data/Mallet_Daten/M_UKS/mallet.topic_keys.8"
td = "/Users/estern/Documents/BA_Data/Mallet_Daten/M_UKS/mallet.topic_distributions.8"
ww = "/Users/estern/Documents/BA_Data/Mallet_Daten/M_UKS/mallet.word_weights.8"


### Alle Topics und deren 10 häufigste Wörter ausgeben ###

topic_tw = m.load_topic_word_distributions(ww)
for _topic, _word_probability_dict in topic_tw.items():
    print('Topic', _topic)
    for _word, _probability in sorted(_word_probability_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(round(_probability, 4), '\t', _word)
    print()