import json
import re
import nltk
nltk.download('punkt_tab')

# pdata
def get_book_dict():
    with open ("Code\\OGdataframes_and_Tidying\\sf_books.json", "r") as f:
        data = json.load(f)
    return data
data = get_book_dict()


def get_tokens(data):  
    # english stoplist
    with open("Code\\OGdataframes_and_Tidying\\stoplist.en.txt", "r") as f:
        stoplist = []
        for line in f:
            stoplist.append(line.strip())

    # tokenization and tidying
    for book in data.keys():
        # removing unicode characters
        data[book] = re.sub(r'[^\x00-\x7F]', ' ', data[book])
        # tokenization
        data[book] = nltk.word_tokenize(data[book], language="english")
        # removing punctuation
        data[book] = [word.lower() for word in data[book] if word.isalpha()]
        # removing stop words
        data[book] = [word for word in data[book] if word not in stoplist]
        # removing words that start with ISBN or https
        data[book] = [word for word in data[book] if not word.startswith(("ISBN", "https"))]
    return data
data = get_tokens(data)

# .txt file with book descriptions
testo = []
for descr in data.values():
    for parola in descr:
        if len(parola)>=3:
            testo.append(parola)
testo_str = " ".join(testo)
with open("Code\\OGdataframes_and_Tidying\\descriptions.txt", "w", encoding="utf-8") as f:
    f.write(testo_str)

# description stemming
def stem(book_dict):
    stemmer = nltk.PorterStemmer()
    for book in book_dict.keys():
        stemmed_words = []
        for word in book_dict[book]:
            stemmed_words.append(stemmer.stem(word))
        book_dict[book] = stemmed_words
    return book_dict
stemmed = stem(data)
# saving stemmed description in a .json file
with open("Code\\OGdataframes_and_Tidying\\stemmed_descr.json", "w") as f:
    json.dump(stemmed, f)
