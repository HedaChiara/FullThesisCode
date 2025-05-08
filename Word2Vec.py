import json
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import numpy as np
import polars as pl


# my stemmed descriptions (dictionary of the form {"Title, Author" : list of stemmed words})
with open ("Code\\OGdataframes_and_Tidying\\stemmed_descr.json", "r") as f:
    stemmed_descr = json.load(f)

# list of my stemmed book descriptions
corpus = [stemmed_descr[book] for book in stemmed_descr.keys()]

# training of the Word2Vec model
model = gensim.models.Word2Vec(corpus, vector_size=100, window=5, min_count=1, workers=4)

# Embedding of a single book using the mean of the embeddings of the words in my descriptions
def book_embedding(words, model):
    # word embeddings
    word_vectors = []
    for word in words:
        word_vectors.append(model.wv[word])
    word_vectors = np.array(word_vectors)
    # mean word vector
    return word_vectors.mean(axis=0).tolist()


# All my book embeddings {book : book embedding}
book_embeddings = {}
for book in stemmed_descr.keys():
    book_embeddings[book] = book_embedding(stemmed_descr[book], model)        

# Saving the book embeddings in a .json file
with open("Code\\Word2VecBookEmbeddings.json", "w") as f:
    json.dump(book_embeddings, f)

with open("Code\\Word2VecBookEmbeddings.json", "r") as f:
    book_embeddings = json.load(f)

# Similarity between two books (cosine similarity)
def book_similarity(book_embedding, other_book_embedding):
    return cosine_similarity(np.array(book_embedding).reshape(1,-1), 
                             np.array(other_book_embedding).reshape(1,-1))[0][0]

# getting rid of problematic books (they probably escaped the english description filter)
nan_books = []
for book in book_embeddings.keys():
    if np.any(np.isnan(book_embeddings[book])):
        nan_books.append(book)
for book in nan_books:
    book_embeddings.pop(book)


# Recommender function
def recommend_w2v(given_book, k=10):
    similarities = {}
    # top k most similar books 
    # initialization
    top_k_titles = [given_book] * k
    similarities[given_book] = [0]
    # dictionary of the form {book : similarity to given_book}
    for book in book_embeddings.keys():
        if book != given_book:
            # similarity between given_book and current book
            similarities[book] = book_similarity(book_embeddings[given_book], book_embeddings[book]) 
            # comparing top k similarities
            for i in range(len(top_k_titles)):
                if similarities[book] > similarities[top_k_titles[i]]:
                    top_k_titles[i] = book
                    break
    return top_k_titles


# recommendation dict I will need for the evaluation

positive_ratings = pl.read_csv("Code\PositiveRatings.csv")

# dictionary of the form {book : [recommended books]}    
# only for rated books
'''
W2Vrecs = {}
i=0
for book in stemmed_descr.keys():
    if book in positive_ratings["Book"].to_list():
        W2Vrecs[book] = recommend_w2v(book)
        i += 1
        print(i)


# saving recs in a .json file
with open("Code\\Word2Vecrecs.json", "w") as f:
    json.dump(W2Vrecs, f)

'''



'''
# Visualization of Word2Vec embeddings of my books
# TSV format for TensorFlow Projector
with open("Code\\Word2Vec.tsv", "w", encoding="utf-8") as vec_file, open("Code\\metadata.tsv", "w", encoding="utf-8") as meta_file:
    for word in model.wv.index_to_key:  # words in the vocabulary
        vector = model.wv[word]
        vec_file.write("\t".join(map(str, vector)) + "\n")  # saves the vectors
        meta_file.write(word + "\n")  # saves the corresponding words


# representation of "1984" only
with open ("Code\\OGdataframes_and_Tidying\\sf_books.json", "r") as f:
    books = json.load(f)
orw = [books["1984, George Orwell"]]
orw_model = gensim.models.Word2Vec(orw, min_count=1, sg=0) # sg=0 per CBOW, sg=1 per Skip-gram
with open("Code\\1984Word2Vec.tsv", "w", encoding="utf-8") as vec_file, open("Code\\1984metadata.tsv", "w", encoding="utf-8") as meta_file:
    for word in orw_model.wv.index_to_key:  # words in the vocabulary
        vector = orw_model.wv[word]
        vec_file.write("\t".join(map(str, vector)) + "\n")  # saves the vectors
        meta_file.write(word + "\n")  # saves the corresponding words

'''

