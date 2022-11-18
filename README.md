# What makes a movie successful?
**Examining the relation between characteristics of movies and their box office revenue with an emphasis on factors like diversity and gender**

## Abstract

The movie business is a multi-billion-dollar industry. Therefore, it would be very beneficial to know what sells and what does not, which is why we want to examine which characteristics of movies and their characters are causing high movie box office revenue. In order to add to this mainly capitalistic driven topic some more societal relevance, during the examination of these characteristics we lay an emphasis on factors like ethnical diversity, gender ratio, and the age distribution between men and women in the cast and how it changed over the years. Because movies can be seen as a reflection of their time, the results of this analysis can act as an indicator for changes and advancements in society over time.

## Research Questions

-	Which characteristics of movies are causing high movie box office revenue?
-	Which characteristics of movies are causing low movie box office revenue?
-	Are there differences in these characteristics between movies from the US and movies from the rest of the world?
-	Did ethnical diversity in successful movies change over time?
-	Did the gender ratio of the cast in successful movies change over time?
- Did the age distribution of men and women of the cast in successful movies change over time?
- What could have caused these changes?
- What can you infer from these changes about society?

## Proposed additional datasets

In addition to the CMU dataset, we want to add the ["The Movies Dataset"](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) from Kaggle.
This dataset contains information on 45,000 movies and it will add **TODO: add number** previously unknown values for the movie box office revenue. It also introduces new features which will be very interesting and beneficial for our further analysis, like for example the budget of a movie. A detailed description of the format and all further relevant information can be found on Kaggle.

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

**Step 3: Searching for further patterns regarding the movie box office revenue (in preparation for step 4)**
- Decide which features will be useful (**TODO: Add list of useful features**)
- Process the features to be interpretable by the Machine Learning model (**TODO: Add processing steps (e.g. dummy variables)**)

**Step 4: Train the regressor/classifier on movie box office revenue data**

**Step 5: Create a datastory presenting the results**

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
