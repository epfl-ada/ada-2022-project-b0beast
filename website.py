import sys
import os
import pickle
import ast
import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import tensorflow as tf

from data_wrangling_tools import *

# Neural Networks
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, RobustScaler, Normalizer
from sklearn.model_selection import train_test_split


from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

st.title("Does diversity pay off? Try it out!")
# Select release year
release_year = st.slider('Select release year', 2000, 2019, 2010)

# Select budget
budget = st.slider('Select budget (Million $)', 0, 300, 100)

# Select runtime
runtime = st.slider('Select runtime (minutes)', 0, 300, 120)

# Select white ratio
white_ratio = st.slider('Select white ratio', 0.0, 1.0, 0.5)

# Select black african american ratio
black_african_american_ratio = st.slider('Select black african american ratio', 0.0, 1.0, 0.5)

# Select asian ratio
asian_ratio = st.slider('Select asian ratio', 0.0, 1.0, 0.5)

# Select native american ratio
native_american_ratio = st.slider('Select native american ratio', 0.0, 1.0, 0.5)

# Select hispanic ratio
hawaiian_ratio = st.slider('Select hawaiian ratio', 0.0, 1.0, 0.5)

# Select other ratio
other_ratio = st.slider('Select other ratio', 0.0, 1.0, 0.5)

# Select male ratio
male_ratio = st.slider('Select male ratio' , 0.0, 1.0, 0.5)

# Select female ratio
female_ratio = st.slider('Select female ratio', 0.0, 1.0, 0.5)

# Select actor age mean
mean_actor_age = st.slider('Select mean actor age', 0, 80, 40)


# Select actor age std
std_actor_age = st.slider('Select std actor age', 0, 10, 5)


# Select actor height mean
mean_actor_height = st.slider('Select mean actor height', 1.5, 2.1, 1.8)


# # Select actor height std
std_actor_height = st.slider('Select std actor height', 0.0, 0.4, 0.1)

# Select genres
genres = [
    'Drama',
    'Comedy',
    'Thriller',
    'Action',
    'Romance Film',
    'Action/Adventure',
    'Adventure',
    'Crime Fiction',
    'Fantasy',
    'Family Film',
    'Romantic comedy',
    'Science Fiction',
    'Period piece',
    'Mystery',
    'Film adaptation',
    'Crime Thriller',
    'Indie',
    'Horror',
    'Comedy-drama',
    'Romantic drama',
    'Animation',
    'Teen',
    'Psychological thriller',
    'War film',
    "Children's/Family",
    'Parody',
    'Black comedy',
    'Musical',
    'Coming of age',
    'Buddy film',
]
selected_genres = st.multiselect('Selecte genres', genres, genres[0:3])

# Select actors
actors = [
    "Samuel L. Jackson",
    "Tom Hanks",
    "Gary Oldman",
    "Eddie Murphy",
    "Alan Rickman",
    "Johnny Depp",
    "Robbie Coltrane",
    "Robert Downey Jr",
    "Morgan Freeman",
    "Orlando Bloom",
    "Maggie Smith",
    "John Cleese",
    "Tom Cruise",
    "Will Smith",
    "Cameron Diaz",
    "Liam Neeson",
    "Tobey Maguire",
    "Warwick Davis",
    "Harry Shearer",
    "Ben Stiller",
    "Stellan Skarsgård",
    "Owen Wilson",
    "Scarlett Johansson",
    "John Rhys-Davies",
    "Emma Watson",
    "Hank Azaria",
    "Daniel Radcliffe",
    "Jamie Waylett",
    "Bonnie Wright",
    "Matt Damon",
    "Richard Griffiths",
    "Leonardo DiCaprio",
    "Christian Bale",
    "Mark Williams",
    "Timothy Spall",
    "Shia LaBeouf",
    "Julia Roberts",
    "Helena Bonham Carter",
    "Jason Isaacs",
    "Giovanni Ribisi",
    "Nicolas Cage",
    "Jack Black",
    "Julie Walters",
    "Arnold Schwarzenegger",
    "Angelina Jolie",
    "Paul Bettany",
    "Dustin Hoffman",
    "Brendan Gleeson",
    "Sylvester Stallone",
    "Elijah Wood",
    "Mike Myers",
    "Zoe Saldana",
    "Kevin McNally",
    "Michael Gambon",
    "Robert De Niro",
    "Emma Thompson",
    "John Leguizamo",
    "Jim Carrey",
    "Brad Garrett",
    "Mark Ruffalo",
    "Denis Leary",
    "Harrison Ford",
    "Bill Nighy",
    "Chris Rock",
    "James Franco",
    "Chris Evans",
    "Gwyneth Paltrow",
    "Michelle Rodriguez",
    "Queen Latifah",
    "Seth Rogen",
    "Sam Worthington",
    "David Cross",
    "Jon Voight",
    "Jonathan Pryce",
    "Julie Andrews",
    "Viggo Mortensen",
    "Jada Pinkett Smith",
    "Ian Holm",
    "Liv Tyler",
    "George Clooney",
    "John Travolta",
    "Anne Hathaway",
    "Alec Baldwin",
    "Michael Clarke Duncan",
    "Fiona Shaw",
    "Jim Broadbent",
    "Laz Alonso",
    "Tyrese Gibson",
    "Peter Jackson",
    "Ray Winstone",
    "David Thewlis",
    "Hugh Jackman",
    "Wes Studi",
    "Anthony Hopkins",
    "Kirsten Dunst",
    "Pierce Brosnan",
    "Lawrence Makoare",
    "Keanu Reeves",
    "Danny DeVito",
    "Stan Lee",
]
selected_actors = st.multiselect('Selecte actors', actors, actors[0:3])

input = {}
input["release_date"] = release_year
input["budget_inflation"] = budget * 1e6
input["runtime"] = runtime
input["white_ratio"] = white_ratio
input["black_african_american_ratio"] = black_african_american_ratio
input["asian_ratio"] = asian_ratio
input["american_indian_alaska_native_ratio"]: native_american_ratio
input["native_hawaiian_other_pacific_islander_ratio"] = hawaiian_ratio
input["other_ratio"] = other_ratio
input["m_ratio"] = male_ratio
input["f_ratio"] = female_ratio
input["a_age_at_release_mean"] = mean_actor_age
input["a_age_at_release_std"] = std_actor_age
input["a_height_mean"] = mean_actor_height
input["a_height_std"] = std_actor_height

for genre in genres:
    if genre in selected_genres:
        input[f"genre:{genre}"] = 1.0
    else:
        input[f"genre:{genre}"] = 0.0

for actor in actors:
    if actor in selected_actors:
        input[f"actor:{actor}"] = 1.0
    else:
        input[f"actor:{actor}"] = 0.0

st.write("Current input: ")
st.write(pd.DataFrame(input, index=[0]))

# Load model
model = tf.keras.models.load_model("model.h5")
#y_pred = model.predict(x_test)