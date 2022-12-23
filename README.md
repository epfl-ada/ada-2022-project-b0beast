# Does Diversity Pay Off?
**Examining the relation between characteristics of movies and their box office revenue with an emphasis on diversity factors like ethncitiy, age, and gender**

## Abstract
After in 2015 all 20 oscar acting nominations were awarded to white people, the [#OscarsSoWhite](https://mobile.twitter.com/search?q=%23oscarssowhite) hastag, criticising the lack of diversity and calling for changes in the film industry, went viral. But should the film industry comply with these demands purely for ethical reasons, or does the film industry benefit from a more diverse cast also from a capitalistical point of view? To investigate whether a more diverse cast attracts a larger audience and thus achieves more financial success, we examine the box office revenue of the films in the ["CMU Movie Summary Corpus"](http://www.cs.cmu.edu/~ark/personas/) dataset. As a measure of diversity, we focus mainly on ethnicity, gender, and age. In particular, we are interested in whether moviegoers' acceptance or rejection for movies with a more diverse cast has changed over the last 100 years. Since movies produced in the US have the biggest audience and make by far the most money, we'll restrict our analysis on those movies.
 
## Research Questions

- Which characteristics of movies are correlated with the movie box office revenue?
-	Did ethnical diversity in successful movies change over time?
-	Did the gender ratio of the cast in successful movies change over time?
- Did the age distribution of men and women of the cast in successful movies change over time?

## Additional datasets

In addition to the CMU dataset, we want to add "movies_metadata.csv" from the ["The Movies Dataset"](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) from Kaggle.
This dataset contains information on 45,000 movies released on or before July 2017. By doing a left join with the existing dataset we managed to add 1074 previously unknown values for the movie box office revenue. That's an increase by 12,78% to a total of 9475 known box office revenue values. It also introduces new features which will be very interesting and beneficial for our further analysis, like for example the budget of a movie. A detailed description of the format and all further relevant information can be found on Kaggle.

## Files
- main.ipynb:: The main notebook. Contains data wrangling, data analysis, graph generations and explanations.
- machine_learning_training.ipynb:: Prepare the data, train the machine learning model and export it for the machine learning website.
- website.py:: The Steamlit website source code that loads the machine learning model and outputs box office revenue predictions.
- gen_ethnicities.ipynb:: Get ethnicities from wikidata using sparql query.
- data_wrangling_tools.py:: Functions to easily load the cleaned datasets.
- ml_tools.py:: Useful functions shared by the machine learning files.
- requirements.txt:: pip requirement file for the machine learning website
- model/:: Trained machine learning model and python pickle files for the machine learning website

- data/:: Folder for the for the raw datasets
- gen/ethnicities.tsv:: Cointains all ethnicities and freebase ID's
- gen/plots:: Folder containing plots exported for the data story website.
- gen/reports:: Folder which cointains reports created with [pandas profiling](https://pandas-profiling.ydata.ai)

## Methods

**Step 1: Data Wrangling (see data_wrangling_tools.py and main.ipynb)**
- Extract data from ethnicities, characters, and movie datasets
- Transform dates in the data from strings to datetime objects
- Remove Freebase ID from features in JSON-format (e.g. language, countries, genres)
- Remove NaN values from various features in a context dependent manner in order to keep as much data as possible for the later analysis
- Extract ethnicities names using SPARQL in python (see gen_ethnicites.ipynb)
- Cluster ethnicites into five groups (for later usage)
- Merge the data (including the additional dataset)

**Step 2: Data Exploration (see main.ipynb)**
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
- [https://janepfl.github.io/](https://janepfl.github.io/)

**Step 5: (bonus) Train a machine learning model to predict box office revenue**
- Clean and augment the data with one-hot encoding on relevant features
- Create a simple deep neural network
- Train the deep neural network on a dataset of around 5000 movies
- Upload the resulting model on an interactive (external) website for users to play with

## Organization within the team

Colin: Exploratory Data Analysis, Data Cleaning, Data Preprocessing, Data Visualization

Matthieu: Machine Learning model and predictions

Hendrik: Fighting the confounders and implementing statistical tests

Jan: Creating the website and write the datastory
