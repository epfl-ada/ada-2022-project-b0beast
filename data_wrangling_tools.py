import pandas as pd
import numpy as np
import ast

def load_characters(character_file):
    character_columns = ['wiki_movie_id', 'freebase_movie_id', 'm_release_date', 'name', 'a_dob', 'a_gender', 'a_height', 'a_ethnicity_freebase_id', 'a_name', 'a_age_at_release', 'freebase_char/a_map', 'freebase_char_id', 'freebase_a_id']
    characters = pd.read_csv(character_file, sep='\t', names=character_columns, index_col=False)

    # convert date string to datetime objects
    characters['m_release_date'] = pd.to_datetime(characters['m_release_date'], format='%Y-%m-%d', errors='coerce')

    return characters


def load_ethnicities(ethnicity_file):
    return pd.read_csv(ethnicity_file, sep='\t', header=None, names=['freebase_ethnicity_id', 'ethnicity_name'])


def add_characters_ethnicities(characters, ethnicities):
    df = characters.copy()
    df = pd.merge(left=characters, right=ethnicities, left_on='a_ethnicity_freebase_id', right_on='freebase_ethnicity_id', how='left')
    df = df.drop(['freebase_ethnicity_id'], axis=1)
    df = df.rename({'a_ethnicity_freebase_id': 'freebase_ethnicity_id'})

    return df


def load_movies(movies_file):
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

    def extract_feature(json):
        """
            Replace json dictionnaries with list of their values
        """
        if json is np.nan:
            return np.nan
        return list(ast.literal_eval(json).values())

    df = df_input.copy()
    
    for feature in features:
        df[feature] = df[feature].apply(extract_feature)

    return df


def load_imdb(imdb_file, columns=['original_title', 'revenue', 'budget', 'vote_average', 'vote_count']):
    imdb = pd.read_csv(imdb_file, usecols=columns)

    # remove wrongly formatted rows (only 3)
    imdb = imdb.drop(imdb[imdb['budget'].str.contains('.jpg')].index)

    # convert numerical columns to float
    imdb['revenue'] = imdb['revenue'].astype(float).apply(lambda x: np.nan if x == 0.0 else x)
    imdb['budget'] = imdb['budget'].astype(float).apply(lambda x: np.nan if x == 0.0 else x)

    return imdb


def merge_characters_movies(characters, movies):
    # Movies and characters
    df = pd.merge(left=characters, right=movies, on='wiki_movie_id', how='left', suffixes=('_c', '_m'))

    # clean features
    duplicate_columns = ['freebase_movie_id_c', 'release_date']
    df = df.drop(duplicate_columns, axis=1)
    df = df.rename(columns={'freebase_movie_id_m': 'freebase_movie_id', 'name_c': 'char_name', 'name_m': 'movie_name', 'ethnicity_name': 'a_ethnicity', 'm_release_date': 'release_date'})

    # change order of columns
    df = df[['wiki_movie_id','freebase_movie_id','movie_name','release_date','box_office_revenue','runtime','genres','languages','countries','char_name','a_name','a_gender','a_ethnicity','a_dob','a_age_at_release','a_height','freebase_char/a_map','freebase_char_id','freebase_a_id','a_ethnicity_freebase_id']]

    return df


def merge_movies_imdb(movies, imdb):
    df = pd.merge(movies, imdb, left_on='name', right_on='original_title', how='left')

    # drop movies that have been duplicated during the merge TODO see it
    df = df.drop_duplicates(subset=['name', 'vote_count', 'vote_average'])

    # fill the box_office revenue with the imdb revenue if it's missing
    df['box_office_revenue'] = df['box_office_revenue'].fillna(df['revenue'].copy())
    df = df.drop(columns=['revenue', 'original_title'])

    return df


def generate_clean_df(character_file, ethnicity_file, movie_file):
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


def generate_clean_df_with_imdb(character_file, ethnicity_file, movie_file, imdb_file):
    # characters
    characters = load_characters(character_file)
    ethnicities = load_ethnicities(ethnicity_file)
    characters = add_characters_ethnicities(characters, ethnicities)

    # movies
    movies = load_movies(movie_file)
    movies = clean_unknowns(movies)
    movies = clean_jsons(movies)

    # imdb movies
    imdb = load_imdb(imdb_file)

    # merge movies and imdb movies
    df = merge_movies_imdb(movies, imdb)

    # merge movies and characters
    df = merge_characters_movies(characters, df)

    return df