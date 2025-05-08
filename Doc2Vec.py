import gensim
import json
import polars as pl


def get_json(filename):
    with open (filename, "r") as f:
        data = json.load(f)
    return data
stemmed_descr = get_json("Code\\OGdataframes_and_Tidying\\stemmed_descr.json")


# TaggedDocuments that will be fed to the model
docs = []
for book in stemmed_descr.keys():
    docs.append(gensim.models.doc2vec.TaggedDocument(words=stemmed_descr[book], tags=[book]))
# model
model = gensim.models.doc2vec.Doc2Vec(docs)
model.save("Code\\Models\\Doc2Vec.model")


# TSV format for TensorFlow Projector
with open("Code\\Doc2Vec.tsv", "w", encoding="utf-8") as vec_file, open("Code\\metadata_doc2vec.tsv", "w", encoding="utf-8") as meta_file:
    for word in model.wv.index_to_key:  # words in the vocabulary
        vector = model.wv[word]
        vec_file.write("\t".join(map(str, vector)) + "\n")  # saves the vectors
        meta_file.write(word + "\n")  # saves the corresponding words

# Recommender function
def recommend(given_book, model=model, k=10):
    # given_book vector
    book_vec = model.infer_vector(stemmed_descr[given_book])
    # k+1 most similar books (the 1st will be given_book)
    topk = model.dv.most_similar(positive=[book_vec], topn=k+1)
    # titles
    titles = []
    for i in range(len(topk)):
        titles.append(topk[i][0])
    return titles[1:]


# {book : top k most similar books}
sim = {}
i=0
for book in stemmed_descr.keys():
    sim[book] = recommend(book)
    i+=1
    print(i)
            
with open("Code\\Doc2Vecrecs.json", "w") as f:
    json.dump(sim, f)

