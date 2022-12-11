import pandas as pd
import numpy as np
import ast

#
# DATASET LOADING
#

def load_characters(character_file):
    """
        TODO fill it
    """
    character_columns = ['wiki_movie_id', 'freebase_movie_id', 'm_release_date', 'name', 'a_dob', 'a_gender', 'a_height', 'a_ethnicity_freebase_id', 'a_name', 'a_age_at_release', 'freebase_char/a_map', 'freebase_char_id', 'freebase_a_id']
    characters = pd.read_csv(character_file, sep='\t', names=character_columns, index_col=False)

    # convert date string to datetime objects
    characters['m_release_date'] = pd.to_datetime(characters['m_release_date'], format='%Y-%m-%d', errors='coerce')

    # drop useless columns
    characters = characters.drop(['freebase_char/a_map', 'freebase_char_id', 'freebase_a_id'], axis=1)

    return characters


def load_ethnicities(ethnicity_file, etchnicity_clusters={1: 'White', 2: 'Black', 3: 'Asian', 4: 'Latino', 5: 'Native / Indigenous people'}):
    """
        TODO fill it
    """
    ethnicities = pd.read_csv(ethnicity_file, sep='\t', header=None, names=['freebase_ethnicity_id', 'ethnicity_name', 'cluster_id'])
    ethnicities['ethnicity_cluster_name'] = ethnicities['cluster_id'].map(etchnicity_clusters)
    return ethnicities


def add_characters_ethnicities(characters, ethnicities):
    """
        TODO fill it
    """
    df = characters.copy()
    df = pd.merge(left=characters, right=ethnicities, left_on='a_ethnicity_freebase_id', right_on='freebase_ethnicity_id', how='left')
    df = df.drop(['a_ethnicity_freebase_id', 'freebase_ethnicity_id', 'ethnicity_name', 'cluster_id'], axis=1)
    df = df.rename(columns={'ethnicity_cluster_name': 'a_ethnicity'})

    return df


def load_movies(movies_file):
    """
        TODO fill it
    """
    movies_columns = ['wiki_movie_id', 'freebase_movie_id', 'name', 'release_date', 'box_office_revenue', 'runtime', 'languages', 'countries', 'genres']
    movies = pd.read_csv(movies_file, sep='\t', names=movies_columns) 

    # clean dates
    movies['release_date'] = pd.to_datetime(movies['release_date'], format='%Y-%m-%d', errors='coerce')

    return movies


def clean_unknowns(input_df, features=['countries', 'genres', 'languages']):
    """
        Replace unkown values in countries, genres and languages
    """

    def replace_unknown(df, label):
        """
            Replace emtpy json with "Unknown"
        """
        return df[label].replace("{}", "{\"\": \"Unknown\"}")
    
    df = input_df.copy()

    for feature in features:
        df[feature] = replace_unknown(df, feature)

    return df


def clean_jsons(df_input, features=['countries', 'genres', 'languages']):
    """
        Replace json dictionnaries for countries, genres and languages
    """

    def extract_feature(json_):
        """
            Replace json dictionnaries with list of their values
        """
        if json_ is np.nan:
            return np.nan
        return list(ast.literal_eval(json_).values())

    df = df_input.copy()
    
    for feature in features:
        df[feature] = df[feature].apply(extract_feature)

    return df


def load_kaggle(kaggle_file, columns=['original_title', 'revenue', 'budget', 'vote_average', 'vote_count', 'release_date']):
    """
        TODO fill it
    """
    kaggle = pd.read_csv(kaggle_file, usecols=columns)

    # remove wrongly formatted rows (only 3)
    kaggle = kaggle.drop(kaggle[kaggle['budget'].str.contains('.jpg')].index)

    # convert date string to datetime objects
    kaggle['release_date'] = pd.to_datetime(kaggle['release_date'], format='%Y-%m-%d', errors='coerce')

    # convert numerical columns to float
    kaggle['revenue'] = kaggle['revenue'].astype(float).apply(lambda x: np.nan if x == 0.0 else x)
    kaggle['budget'] = kaggle['budget'].astype(float).apply(lambda x: np.nan if x == 0.0 else x)

    return kaggle


def merge_characters_movies(characters, movies):
    """
        TODO fill it
    """
    # Movies and characters
    df = pd.merge(left=characters, right=movies, on='wiki_movie_id', how='left', suffixes=('_c', '_m'))

    # clean features
    duplicate_columns = ['freebase_movie_id_c', 'release_date']
    df = df.drop(duplicate_columns, axis=1)
    df = df.rename(columns={'freebase_movie_id_m': 'freebase_movie_id', 'name_c': 'char_name', 'name_m': 'movie_name', 'm_release_date': 'release_date'})

    # change order of columns
    df = df[['wiki_movie_id','freebase_movie_id','movie_name','release_date','box_office_revenue','runtime','genres','languages','countries','char_name','a_name','a_gender','a_ethnicity','a_dob','a_age_at_release','a_height']]

    return df


def merge_movies_kaggle(movies, kaggle):
    """
        TODO fill it
    """
    df = pd.merge(movies, kaggle, left_on=[movies['name'], movies['release_date'].dt.year], 
        right_on=[kaggle['original_title'], kaggle['release_date'].dt.year], how='left')
    df = df.rename({'release_date_x': 'release_date'}, axis=1)

    # fill the box_office revenue with the kaggle revenue if it's missing
    df['box_office_revenue'] = df['box_office_revenue'].fillna(df['revenue'].copy())
    df = df.drop(columns=['revenue', 'original_title', 'key_0', 'key_1', 'release_date_y'])
    
    return df


def generate_clean_df(character_file, ethnicity_file, movie_file):
    """
        TODO fill it
    """
    # characters
    characters = load_characters(character_file)
    ethnicities = load_ethnicities(ethnicity_file)
    characters = add_characters_ethnicities(characters, ethnicities)

    # movies
    movies = load_movies(movie_file)
    movies = clean_unknowns(movies)
    movies = clean_jsons(movies)

    # merge
    df = merge_characters_movies(characters, movies)

    return df


def generate_clean_df_with_kaggle(character_file, ethnicity_file, movie_file, kaggle_file):
    """
        TODO fill it
    """
    # characters
    characters = load_characters(character_file)
    ethnicities = load_ethnicities(ethnicity_file)
    characters = add_characters_ethnicities(characters, ethnicities)

    # movies
    movies = load_movies(movie_file)
    movies = clean_unknowns(movies)
    movies = clean_jsons(movies)

    # kaggle movies
    kaggle = load_kaggle(kaggle_file)

    # merge movies and kaggle movies
    df = merge_movies_kaggle(movies, kaggle)

    # merge movies and characters
    df = merge_characters_movies(characters, df)

    return df


#
# DATA ANALYSIS
#

def filter_with_countries(df, target_countries, mode):
    """
        TODO fill it
    """
    # TODO drop na on every columns ?
    if mode == 'all':
        return df[df["countries"].apply(lambda x: all(country in x for country in target_countries))]
    elif mode == 'any':
        return df[df["countries"].apply(lambda x: any(country in x for country in target_countries))]
    elif mode == 'only':
        return df[df["countries"].apply(lambda x: set(x) == set(target_countries))]
    else:
        raise ValueError('mode must be one of [all, any, only]')

