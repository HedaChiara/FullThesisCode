import polars as pl

# 12 original book dataframes
alien = pl.read_csv("sf_aliens.csv")
alt_hist = pl.read_csv("sf_alternate_history.csv")
alt_uni = pl.read_csv("sf_alternate_universe.csv")
apo = pl.read_csv("sf_apocalyptic.csv")
cpunk = pl.read_csv("sf_cyberpunk.csv")
dyst = pl.read_csv("sf_dystopia.csv")
hard = pl.read_csv("sf_hard.csv")
mil = pl.read_csv("sf_military.csv")
robots = pl.read_csv("sf_robots.csv")
space = pl.read_csv("sf_space_opera.csv")
steam = pl.read_csv("sf_steampunk.csv")
ttravel = pl.read_csv("sf_time_travel.csv")

books = pl.concat([alien, alt_hist, alt_uni, apo, cpunk, dyst, hard, mil, robots, space, steam, ttravel])
books.write_csv("concat_books.csv")

# 12 genre indicator variables
n = books.shape[0]
I_alien = [0] * n
I_alt_hist = [0] * n
I_alt_uni = [0] * n
I_apo = [0] * n
I_cpunk = [0] * n
I_dyst = [0] * n
I_hard = [0] * n
I_mil = [0] * n
I_robots = [0] * n
I_space = [0] * n
I_steam = [0] * n
I_ttravel = [0] * n
# Indicator variable titles
new_columns = [I_alien, I_alt_hist, I_alt_uni, I_apo, I_cpunk, I_dyst, I_hard, I_mil, I_robots, I_space, I_steam, I_ttravel]
# List of genres
genres = [alien, alt_hist, alt_uni, apo, cpunk, dyst, hard, mil, robots, space, steam, ttravel]
len_genres = [genre.shape[0] for genre in genres]
# Creating indicator variables
k = 0
for i in range(0, len(new_columns)):
    # metto 1 al posto di 0 nelle posizioni da k a k + numero di libri appartenenti al genere corrente
    new_columns[i][k : k + len_genres[i]] = [1] * len_genres[i]
    # aggiorno k aggiungendo il numero di libri appartenenti al genere corrente
    k += len_genres[i]

books = books.drop(["Genres", "Original_Book_Title"])
books = books.with_columns([pl.Series(name="I_alien", values=I_alien),
                            pl.Series(name="I_alt_hist", values=I_alt_hist),
                            pl.Series(name="I_alt_uni", values=I_alt_uni),
                            pl.Series(name="I_apo", values=I_apo),
                            pl.Series(name="I_cpunk", values=I_cpunk),
                            pl.Series(name="I_dyst", values=I_dyst),
                            pl.Series(name="I_hard", values=I_hard),
                            pl.Series(name="I_mil", values=I_mil),
                            pl.Series(name="I_robots", values=I_robots),
                            pl.Series(name="I_space", values=I_space),
                            pl.Series(name="I_steam", values=I_steam),
                            pl.Series(name="I_ttravel", values=I_ttravel)
                            ])

books = books.with_columns(
    pl.col("url").str.strip_chars(),
    pl.col("Book_Title").str.strip_chars(),
    pl.col("Author_Name").str.strip_chars(),
    pl.col("Book_Description").str.strip_chars()
    )          
                
# getting rid of books that appear multiple times
no_duplicates = books.group_by(["Book_Title", "Author_Name", "Edition_Language", "Rating_score", "Rating_votes", "Review_number", "Book_Description", "Year_published", "url"]
                       ).agg([pl.col(["I_alien", "I_alt_hist", "I_alt_uni", "I_apo", "I_cpunk", "I_dyst", "I_hard", "I_mil", "I_robots", "I_space", "I_steam", "I_ttravel"])
                       .sum()])

# they have not all been removed yet, there are some discrepancies in the data -> I'm keeping the most recent
recent = (
    no_duplicates.sort(
        by = "Rating_votes", descending=True)
        .unique(
            ["Book_Title", "Author_Name"],  keep = "first", maintain_order = True)
        .select(["Book_Title","Author_Name","Rating_score", "Book_Description"])
)

no_duplicates = (
    no_duplicates.filter(pl.col("Edition_Language").is_in(["English", "None"]))
    .sort(by = "Rating_votes", descending=True).group_by(
    ["Book_Title", "Author_Name"]
    ).agg(
        pl.col("Rating_votes").max(),
        pl.col("Review_number").max(),
        pl.col("Year_published").min(), 
        pl.col(["I_alien", "I_alt_hist", "I_alt_uni", "I_apo", "I_cpunk", "I_dyst", "I_hard", "I_mil", "I_robots", "I_space", "I_steam", "I_ttravel"])
        .sum()
        # joining most recent data
        ).join(recent, on = ["Book_Title", "Author_Name"], how = "inner")
)

no_duplicates.write_csv("sf_books_tidy.csv")