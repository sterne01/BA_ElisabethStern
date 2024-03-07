# Für das POS-Tagging & Lemmatisieren
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import glob
# Für das Topic Modelling:
import little_mallet_wrapper as m

### Stimmt mit dem Code in "BA_POS_and_Topics_UKMen" überein. Vollständige Annotationen in "BA_POS_and_Topics_UKMen".
### TEXT PREPROCESSING ###
nltk.download("stopwords")

path = "/Users/estern/Documents/BA_Data/F_UKS_Lyr/"

lyricsstrings = []

print("Anzahl der Lyricsdokumente: ", len(glob.glob(path+"*")))

for file in sorted(glob.glob(path+"*")):
    with open(file, 'r') as f:
        data = f.read()
        lyricsstrings.append(str(data))

lemma = WordNetLemmatizer()

lemmatized = []
for string in lyricsstrings:
    l = ""
    for word in word_tokenize(string):
        l += str(lemma.lemmatize(word)) + " "

    lemmatized.append(l)

tokenized = []
for word in lemmatized:
    tokenized.append(nltk.pos_tag(word_tokenize(word.lower()), tagset="universal"))

topicslist = []
for song in tokenized:
    newstring = ""
    for taggedword in song:
        if taggedword[1] == "NOUN":
            newstring += taggedword[0] + " "
        elif taggedword[1] == "ADJ":
            newstring += taggedword[0] + " "

    topicslist.append(newstring)

# print("Nouns and Adjectives for Topic Modelling:", topicslist) # kann ausgegeben werden, falls eine Übersicht erwünscht ist


### TOPIC MODELLING ###
path_mallet = "/Applications/mallet-2.0.8/bin/mallet"
path_output = "/Users/estern/Documents/BA_Data/Mallet_Daten/F_UKS"

training_data = topicslist
training_data = [m.process_string(t, stop_words=stopwords.words("english Kopie"), remove_punctuation=True)
                 for t in training_data]

# Anfang der Trainingsdaten anzeigen, falls erwünscht
# print(training_data[0])


topic_keys, topic_distributions = m.quick_train_topic_model(path_to_mallet=path_mallet,
                                                            output_directory_path=path_output, num_topics=10,
                                                            training_data=training_data)


tk = "/Users/estern/Documents/BA_Data/Mallet_Daten/F_UKS/mallet.topic_keys.10"
td = "/Users/estern/Documents/BA_Data/Mallet_Daten/F_UKS/mallet.topic_distributions.10"
ww = "/Users/estern/Documents/BA_Data/Mallet_Daten/F_UKS/mallet.word_weights.10"


topic_tw = m.load_topic_word_distributions(ww)
for _topic, _word_probability_dict in topic_tw.items():
    print('Topic', _topic)
    for _word, _probability in sorted(_word_probability_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(round(_probability, 4), '\t', _word)
    print()