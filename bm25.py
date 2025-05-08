from rank_bm25 import BM25Okapi
import json

# dictionary of my stemmed descriptions
with open ("Code\\OGdataframes_and_Tidying\\stemmed_descr.json", "r") as f:
        stemmed_descr = json.load(f)

corpus = [stemmed_descr[book] for book in stemmed_descr.keys()]

bm25 = BM25Okapi(corpus)


def recommend(given_book, corpus=corpus, k=10):
    # top k+1 most similar descriptions to the given one
    top_k_descriptions = bm25.get_top_n(stemmed_descr[given_book], corpus, n=k+1)
    # retrieving the titles
    top_k_titles = []
    for book in stemmed_descr.keys():
        if stemmed_descr[book] in top_k_descriptions:
            top_k_titles.append(book)
    if given_book in top_k_titles:
        top_k_titles.remove(given_book)
        return top_k_titles
    return top_k_titles[:-1]
        

# dictionary of the form {book : top 50 most similar books}      
sim2 = {}
i=0
for book in stemmed_descr.keys():
    sim2[book] = recommend(book, k=50)
    i+=1
    print(i)
with open("Code\\BM25recs_extended.json", "w") as f:
    json.dump(sim2, f)


















