### FullThesisCode
This repository contains every file necessary for the development and evaluation of the recommender systems I implemented for my Bachelor Degree in Statistics "*From Synopsis to Suggestion: Algorithmic Text-Based Recommendations for Sci-Fi Books*", which set out to develop and compare different text-based recommender systems for science fiction books.

The **OGdataframes_and_Tidying** folder contains all the original dataframes and the code I used to tidy them. In particular:
- files starting with "*sf_*" are the 12 original book dataframes
- files starting with "*user_rating*" are the original user dataframes
- **Tidying.py** contains the code I used to join and tidy the 12 original book dataframes
- **text_mining.py** contains the code I used to work with the textual book descriptions
- **MergeRatings.R** contains the code I used to extract user ratings that involved books in the book dataframe
- **adjustingTitles.py** creates a .json file with user ratings in a more convenient format
- **books2json.py** creates a .json file from a .csv one

The other .py files are the ones involved in the implementation and evaluation of the three recommender systems:
- **Word2Vec.py** trains the Word2Vec based RS
- **Doc2Vec.py** trains the Doc2Vec based RS
- **bm25.py** trains the BM25 based RS
- **evaluatingTextBased** contains the code I used for the evaluation of these RSs

### Web Application
You can access the web application that puts this work into action at https://sci-finder.streamlit.app/
