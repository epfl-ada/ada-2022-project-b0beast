# Does Diversity Pay Off?
**Examining the relation between characteristics of movies and their box office revenue with an emphasis on factors like diversity and gender**

## Abstract
After in 2015 all 20 oscar acting nominations were awared to white people, the #OscarsSoWhite hastag, criticising the lack of diveristy in the film industry, went viral. But should the film industry comply with these demands purely for ethical reasons, or do capitalistically motivated actors in the film industry also benefit from a more diverse cast? To investigate whether a more diverse cast attracts a larger audience and thus achieves more financial success, we examine the box office revenue of the films in the ["CMU Movie Summary Corpus"](http://www.cs.cmu.edu/~ark/personas/) dataset. As a measure of diversity, we focus on ethnicity, gender, and age. In particular, we are interested in whether moviegoers' preference or rejection for movies with a more diverse cast has changed over the last 100 years.
 
 
## Research Questions

-	Which characteristics of movies are causing high movie box office revenue?
-	Which characteristics of movies are causing low movie box office revenue?
-	Are there differences in these characteristics between movies from the US and movies from the rest of the world?
-	Did ethnical diversity in successful movies change over time?
-	Does ethnical diversity correlate with the box office revenue?
-	Did the gender ratio of the cast in successful movies change over time?
- Did the age distribution of men and women of the cast in successful movies change over time?
- What could have caused these changes?
- What can you infer from these changes about society?

## Proposed additional datasets

In addition to the CMU dataset, we want to add "movies_metadata.csv" from the ["The Movies Dataset"](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) from Kaggle.
This dataset contains information on 45,000 movies released on or before July 2017. By doing a left join with the existing dataset we managed to add 1074 previously unknown values for the movie box office revenue. That's an increase by 12,78% to a total of 9475 known box office revenue values. It also introduces new features which will be very interesting and beneficial for our further analysis, like for example the budget of a movie. A detailed description of the format and all further relevant information can be found on Kaggle.

## Files
- data_exploration.ipynb:: Ananlysis on the dataset
- data_wrangling.ipynb:: Load datasets, merge and clean
- gen_ethnicities.ipynb:: Get ethnicities from wikidata using sparql query
- data_wrangling_tools.py:: Functions to easily load the cleaned datasets
- gen/ethnicities.tsv::  Cointains all ethnicities and freebase ID's
- gen/reports:: Folder which cointains reports created with [pandas profiling](https://pandas-profiling.ydata.ai)

## Methods

**Step 1: Data Wrangling (see data_wrangling.ipynb)**
- Extract data from ethnicities, characters, and movie datasets
- Transform dates in the data from strings to datetime objects
- Remove Freebase ID from features in JSON-format (e.g. language, countries, genres)
- Remove NaN values from various features in a context dependent manner in order to keep as much data as possible for the later analysis
- Extract ethnicities names using SPARQL in python (see gen_ethnicites.ipynb)
- Cluster ethnicites into five groups (for later usage)
- Merge the data (including the additional dataset)

**Step 2: Data Exploration (see data_exploration.ipynb)**
- Ensure that we have the required amount of valid data needed for our further analysis
- Find patterns in the data regarding gender, ethnicities, and age of the actors
- Plot evolution of gender ratio, ethnical diversity and age distribution of the actors over the decades
- Plot evolution of movie box office revenue in the US

**Step 3: Searching for further patterns regarding the movie box office revenue**
- Divide the data into two groups: With box office revenue, and without.
- Decide which features will be useful: release date, runtime, languages, countries, genres.
- Process the features to be interpretable by the Machine Learning model:
    - Treat outliers
    - Normalize continuous data
    - Apply one-hot encoding to labeled data
- Train and validate several models and compare them on movies with box office revenue
- For compatible models, extract weights and display features that play a big role in box office revenue.
- Predict box office revenue for movies missing it

**Step 4: Create a datastory presenting the results**

## Proposed timeline

- 02.12.22 Homework 2 deadline
- 03.12.22 Start further analysis
- 09.12.22 Discuss open questions in the project office hour
- 10.12.22 Start developing a first draft of the datastory
- 16.12.22 Discuss open questions in the project office hour
- 17.12.22 Finish the analysis
- 19.12.22 Finish the datastory
- 23.12.22 Milestone 3 deadline

## Organization within the team

Split the work into pairs of two:

- Further data analysis & create datastory: Colin, Jan
- Implement and train the Machine Learning model & create website: Hendrik, Matthieu
