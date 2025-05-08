import polars as pl
import json

data = (pl.read_csv("sf_books_tidy.csv").filter(pl.col("Book_Description").is_not_null())
        .filter(pl.col("Author_Name").is_not_null())
        .filter(pl.col("Book_Title").is_not_null())
        .select(["Book_Title", "Author_Name", "Book_Description"])
)
descr_dict = (
    data.write_json()
)

# list of dicts {title:"", author:"", description:""}
descr_dict = json.loads(descr_dict)

# dict {"title, author" : description}
better_descr_dict = {}
for d in descr_dict:
    better_descr_dict[str(d["Book_Title"] + ", " + d["Author_Name"])] = d["Book_Description"]

with open("sf_books.json", "w") as f:
    json.dump(better_descr_dict, f)


