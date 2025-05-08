library(tidyverse)

# tidy book dataframe
books <- read_csv("sf_books_tidy.csv")

# original user dataframes
r0 <- read_csv("user_rating_0_to_1000.csv")
r1 <- read_csv("user_rating_1000_to_2000.csv")
r2 <- read_csv("user_rating_2000_to_3000.csv")
r3 <- read_csv("user_rating_3000_to_4000.csv")
r4 <- read_csv("user_rating_4000_to_5000.csv")
r5 <- read_csv("user_rating_5000_to_6000.csv")
r6 <- read_csv("user_rating_6000_to_11000.csv")
allr <- bind_rows(list(r0, r1, r2, r3, r4, r5, r6))
allr <- allr %>% mutate(Book_Title=str_squish(Name), .before="Rating") %>% select(-c(Name))
allr %>% group_by(ID) %>% summarise(num_rating = n()) 
dim(allr)

# only keeping books in my book dataframe
ratings <- allr %>% inner_join(books, by="Book_Title", relationship="many-to-many") %>% select(ID, Book_Title, Rating)
dim(ratings)

grouped_ratings <- ratings %>% group_by(ID) %>% summarise(num_rating = n())
grouped_ratings %>% select(ID) %>% unique() %>% dim()
# 2607 different users
ratings %>% select(Book_Title) %>% unique() %>% dim()
# 1925 different books 
grouped_ratings %>% select(num_rating) %>% filter(num_rating==1) %>% count()
# 574 users only gave 1 rating
574/2607

mean(grouped_ratings$num_rating)
max(grouped_ratings$num_rating)
which(grouped_ratings$num_rating==190)
ggplot(grouped_ratings) +
  geom_histogram(aes(x=num_rating, y = after_stat(count) / sum(after_stat(count))), bins=100) +
  labs(x = "number of ratings",
       y = "relative frequency") +
  scale_x_continuous(breaks = seq(0, 200, by = 15)) +
  theme_minimal()
# median = 4
quantile(grouped_ratings$num_rating, 0.5)
quantile(grouped_ratings$num_rating, 0.75)
grouped_ratings %>% select(num_rating) %>% count(num_rating>=8)
grouped_ratings %>% select(num_rating) %>% count(num_rating>=4)
# only keeping ratings by users that have rated at least 2 books
grouped_ratings <- grouped_ratings[grouped_ratings$num_rating>1,]
View(grouped_ratings)

my_ratings <- inner_join(ratings, grouped_ratings, by="ID")
# discarding the outlier
my_ratings <- my_ratings %>% filter(num_rating < 190)
View(my_ratings)

my_ratings %>% select(ID) %>% unique() %>% dim()
# 2032 different users
my_ratings %>% select(Book_Title) %>% unique() %>% dim()
# 1890 different books

dim(my_ratings)
# 22281 total ratings
write_csv(my_ratings, "MyRatings.csv")

# positive ratings dataframe
ratings <- read_csv("MyRatings_Book.csv")
positive <- c("liked it", "really liked it", "it was amazing")
positive_ratings <- ratings %>% filter(Rating %in% positive)
View(positive_ratings)
dim(positive_ratings)
positive_ratings %>% select(ID) %>% unique() %>% dim()
positive_ratings %>% select(Book) %>% unique() %>% dim()
write_csv(positive_ratings, "PositiveRatings.csv")

# most rated books
p <- read_csv("PositiveRatings.csv")
grouped_p <- p %>% group_by(Book) %>% summarise(num_rating = n())
grouped_p %>% arrange(-num_rating) %>% View()
