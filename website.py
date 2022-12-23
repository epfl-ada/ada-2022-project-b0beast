import pickle

import pandas as pd
import numpy as np
import streamlit as st
import tensorflow as tf

from data_wrangling_tools import *
from ml_tools import *


from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

st.title("Does diversity pay off? Try it out! \nMake your own movie and see how much it will earn!")

# load genres from pickle
with open('model/genres.pkl', 'rb') as f:
    genres = pickle.load(f)

selected_genres = st.multiselect('Selecte genres', genres, genres[0:7])

# load actors from pickle
with open('model/actors.pkl', 'rb') as f:
    actors = pickle.load(f)

selected_actors = st.multiselect('Selecte actors', actors, actors[0:7])


# load normalizing data from pickle
with open('model/mins.pkl', 'rb') as f:
    mins = pickle.load(f)

with open('model/maxs.pkl', 'rb') as f:
    maxs = pickle.load(f)

with open('model/means.pkl', 'rb') as f:
    means = pickle.load(f)

with open('model/stds.pkl', 'rb') as f:
    stds = pickle.load(f)

with open('model/columns.pkl', 'rb') as f:
    columns = pickle.load(f)

columns.remove("box_office_inflation")

# Select release year
release_year = st.slider('Release year', mins["release_date"], maxs["release_date"], int(means["release_date"]))

# Select budget
budget = st.slider('Budget (million $)', int(mins["budget_inflation"] / 1e6), int(maxs["budget_inflation"] / 1e6), int(means["budget_inflation"] / 1e6))

# Select runtime
runtime = st.slider('Runtime', int(mins["runtime"]), int(maxs["runtime"]), int(means["runtime"]))

# Select white ratio
white_ratio = st.slider('White ratio', 0.0, 1.0, float(means["white_ratio"]))

# Select black african american ratio
black_african_american_ratio = st.slider('Black African American ratio', 0.0, 1.0, float(means["black_african_american_ratio"]))

# Select asian ratio
asian_ratio = st.slider('Asian ratio', 0.0, 1.0, float(means["asian_ratio"]))

# Select native american ratio
native_american_ratio = st.slider('Native American ratio', 0.0, 1.0, float(means["american_indian_alaska_native_ratio"]))

# Select hawaiian ratio
hawaiian_ratio = st.slider('Hawaiian ratio', 0.0, 1.0, float(means["native_hawaiian_other_pacific_islander_ratio"]))

# Select other ratio
other_ratio = st.slider('Other ratio', 0.0, 1.0, float(means["other_ratio"]))

# Select male ratio
male_ratio = st.slider('Male ratio' , 0.0, 1.0, float(means["m_ratio"]))

# Select female ratio
female_ratio = st.slider('Female ratio', 0.0, 1.0, float(means["f_ratio"]))

# Select actor age mean
mean_actor_age = st.slider('Mean actor age', int(mins["a_age_at_release_mean"]), int(maxs["a_age_at_release_mean"]), int(means["a_age_at_release_mean"]))

# Select actor age std
std_actor_age = st.slider('Std actor age', float(mins["a_age_at_release_std"]), float(maxs["a_age_at_release_std"]), float(means["a_age_at_release_std"]))

# Select actor height mean
mean_actor_height = st.slider('Mean actor height', float(mins["a_height_mean"]), float(maxs["a_height_mean"]), float(means["a_height_mean"]))

# # Select actor height std
std_actor_height = st.slider('Std actor height', float(mins["a_height_std"]), float(maxs["a_height_std"]), float(means["a_height_std"]))

input = {}
input["release_date"] = release_year
input["budget_inflation"] = budget * 1e6
input["runtime"] = runtime
input["white_ratio"] = white_ratio
input["black_african_american_ratio"] = black_african_american_ratio
input["asian_ratio"] = asian_ratio
input["american_indian_alaska_native_ratio"]= native_american_ratio
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

df_in = pd.DataFrame(input, index=[0])

st.write("Current input: ")
st.write(df_in)

df_norm = normalize(df_in, columns, mins, maxs)
#df_norm = standardize(df_norm, columns, means, stds)

st.write("Normalized input: ")
st.write(df_norm)

# Load model
model = tf.keras.models.load_model("model/model.h5")

y_pred = model.predict(df_norm)
pred = y_pred[:, 0]

# Denormalize
df_pred = pd.DataFrame({"pred": pred})
df_pred = denormalize_column(df_pred, "pred", mins["box_office_inflation"], maxs["box_office_inflation"])

prediction = int(df_pred.iloc[0, 0])

pos_prediction = max(prediction, 0)

st.title(f"Predicted box office revenue:")
print()
st.title(f"{pos_prediction:_}$".replace("_", "'"))
if prediction < 0:
    st.write(f"(Actually {prediction:_}$)".replace("_", "'"))