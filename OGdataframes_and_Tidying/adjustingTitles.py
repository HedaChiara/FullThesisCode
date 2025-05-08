import polars as pl
import streamlit as st

# I need to append the author to the title of the rated book
ratings = pl.read_csv("Code\\MyRatings.csv")
books = pl.read_csv("Code\\OGdataframes_and_Tidying\\sf_books_tidy.csv")


# I'm assuming that if there are duplicated titles, the one in MyRatings refers to the most popular one
books_agg = books.group_by("Book_Title").agg([
    pl.col("Author_Name").max().alias("author"),  
    pl.col("Rating_votes").max().alias("rating_votes")
])

# merging dataframes
ratings = ratings.join(books_agg, on="Book_Title", how="left")

# creating the column "Book", of the form "Book_Title, Author_Name", like the keys in my book dictionary
ratings = ratings.with_columns(
    (pl.col("Book_Title") + ", " + pl.col("author")).alias("Book"))

# removing unnecessary columns
ratings = ratings.drop(["Book_Title","author", "rating_votes"])
ratings = ratings.select(["ID", "Book", "Rating", "num_rating"])

st.write(ratings)
st.write(ratings.shape)

ratings.write_csv("Code\\MyRatings_Book.csv")





