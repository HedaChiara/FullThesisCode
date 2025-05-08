import json

# dictionary of the form {user_id : [liked books]}
with open ("Code\\PositiveRatings.json", "r") as f:
        ratings = json.load(f)
# Word2Vec recommendations
with open ("Code\\Word2Vecrecs.json", "r") as f:
        W2Vrecs = json.load(f)
# Doc2Vec recommendations
with open ("Code\\Doc2Vecrecs.json", "r") as f:
        D2Vrecs = json.load(f)
# BM25 recommendations
with open ("Code\\BM25recs.json", "r") as f:
        BM25recs = json.load(f)

# Adding some of my personal faves to the rating dictionary, just for fun
ratings["Chiara"] = ["Blindness, José Saramago", "Selected Stories of Philip K. Dick, Philip K. Dick", "Brave New World, Aldous Huxley",
                     "Animal Farm, George Orwell", "1984, George Orwell", "A Game of Thrones, George R.R. Martin", 
                     "It, Stephen King", "11/22/63, Stephen King", "1Q84, Haruki Murakami", "On a Sunbeam, Tillie Walden",
                     "The Island of Doctor Moreau, H.G. Wells", "Flatland: A Romance of Many Dimensions, Edwin A. Abbott"]


# receives the recommendations of a model for a certain book and calculates the cardinality of the intersection between the recommendation set 
# and another set of liked book
# recs are the recommendations given by a certain model for a certain book
def get_intersection_cardinality(recs, liked_books):
        intersection_count = 0
        # checking how many books in my recommendation list are present in the list of the books liked by the user
        for rec in recs:
                if rec in liked_books:
                        intersection_count += 1
        # print(intersection_count)
        return intersection_count

# receives a user id (so it knows the books they liked) and a model's recommendations
def get_mean_cardinality(user_id, model):
        # Leave-One-Out CV
        cardinalities = []
        for book in ratings[user_id]:
                if book in model.keys():
                        recommendations = model[book]

                        # set of the books the user liked-current_book
                        current_liked_set = [b for b in ratings[user_id] if b != book]

                        # getting the intersection cardinalities between the recommendations set and the (liked books\current book) set
                        cardinalities.append(get_intersection_cardinality(recommendations, current_liked_set))
                # I get some KeyErrors if I don't do this (I'll try to fix it)
                else:
                        cardinalities.append(0)

        # returning the mean cardinality for this combination of user and model
        return float(sum(cardinalities) / len(cardinalities)) if cardinalities else 0

'''
# EXAMPLE:
# trying with my books and the top 10 recs from the BM25 model (mean card. should be > 0)
my_liked_books = []
for liked in ratings["Chiara"]:
        my_liked_books.append(liked)
print("Chiara liked the books:", my_liked_books)

sample_BM25 = []
for book in my_liked_books:
        sample_BM25.append(BM25recs[book])

print("BM25 recommends these books: ", sample_BM25)
print("The mean cardinality of the intersection for this user is:", get_mean_cardinality("Chiara", BM25recs))
'''

# returns the recall for a user
def get_recall(user_id, model): 
        len_liked = len(ratings[user_id])
        numerator = get_mean_cardinality(user_id, model)
        return numerator / len_liked


# returns the mean mean cardinality of the intersection between the recommendations set and the (liked books\current book) set for every user
def get_mean_precision_every_user(model):
        cardinalities = []
        for user_id in ratings.keys():
                cardinalities.append(get_mean_cardinality(user_id, model))
        precision = round(float(sum(cardinalities) / (10*len(cardinalities))), 4)
        return precision

def get_mean_recall_every_user(model):
        recalls = []
        for user_id in ratings.keys():
                recalls.append(get_recall(user_id, model))
        # mean recall
        return round(sum(recalls) / len(recalls), 4)


# results
print("Word2Vec's precision for the top 10 recommendations", get_mean_precision_every_user(W2Vrecs))  
print("Doc2Vec's precision for the top 10 recommendations", get_mean_precision_every_user(D2Vrecs))    
print("BM25's precision for the top 10 recommendations", get_mean_precision_every_user(BM25recs))   

print("Word2Vec's recall for the top 10 recommendations", get_mean_recall_every_user(W2Vrecs))  
print("Doc2Vec's recall for the top 10 recommendations", get_mean_recall_every_user(D2Vrecs))    
print("BM25's recall for the top 10 recommendations", get_mean_recall_every_user(BM25recs))   



       
       