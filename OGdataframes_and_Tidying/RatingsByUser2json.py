import polars as pl
import json

# only positive ratings
ratings = pl.read_csv("Code\\PositiveRatings.csv")
ratings = ratings.select(["ID", "Book", "Rating"])

# list of my user IDs
user_ids = ratings["ID"].unique().to_list()

# dictionary of the form { user_id : [liked books]}
rating_dict = {}
for id in user_ids:
    # titles of the books the user liked
    liked_books = ratings.filter(pl.col("ID")==id)
    titles = pl.Series(liked_books.select("Book")).to_list()
    rating_dict[id] = titles

# saving this dictionary in a .json file
with open("Code\\PositiveRatings.json", "w") as f:
    json.dump(rating_dict, f)
    
    

    
















