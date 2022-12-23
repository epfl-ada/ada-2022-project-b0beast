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
    character_columns = [
        "wiki_movie_id",
        "freebase_movie_id",
        "m_release_date",
        "name",
        "a_dob",
        "a_gender",
        "a_height",
        "a_ethnicity_freebase_id",
        "a_name",
        "a_age_at_release",
        "freebase_char/a_map",
        "freebase_char_id",
        "freebase_a_id",
    ]
    characters = pd.read_csv(
        character_file, sep="\t", names=character_columns, index_col=False
    )

    # convert date string to datetime objects
    characters["m_release_date"] = pd.to_datetime(
        characters["m_release_date"], format="%Y-%m-%d", errors="coerce"
    )

    # drop useless columns
    characters = characters.drop(
        ["freebase_char/a_map", "freebase_char_id", "freebase_a_id"], axis=1
    )

    return characters


def load_ethnicities(ethnicity_file, etchnicity_clusters):
    """
        TODO fill it

        Clusters:
        {1: 'White', 
         2: 'Black / African American', 
         3: 'Asian', 
         4: 'American Indian / Alaska Native', 
         5: 'Native Hawaiian / Other Pacific Islander',
         6: 'Other'}
    """
    ethnicities = pd.read_csv(
        ethnicity_file,
        sep="\t",
        header=None,
        names=["freebase_ethnicity_id", "ethnicity_name", "cluster_id", "is_hispanic"],
    )

    ethnicities["ethnicity_cluster_name"] = ethnicities["cluster_id"].map(
        etchnicity_clusters
    )
    ethnicities["is_hispanic"] = (
        ethnicities["is_hispanic"].map({"-": 0, "+": 1}).astype(int)
    )

    return ethnicities


def add_characters_ethnicities(characters, ethnicities):
    """
        TODO fill it
    """
    df = characters.copy()
    df = pd.merge(
        left=characters,
        right=ethnicities,
        left_on="a_ethnicity_freebase_id",
        right_on="freebase_ethnicity_id",
        how="left",
    )
    df = df.drop(
        [
            "a_ethnicity_freebase_id",
            "freebase_ethnicity_id",
            "ethnicity_name",
            "cluster_id",
        ],
        axis=1,
    )
    df = df.rename(
        columns={
            "ethnicity_cluster_name": "a_ethnicity",
            "is_hispanic": "a_is_hispanic",
        }
    )

    return df


def load_cmu_movies(movies_file):
    """
        TODO fill it
    """
    movies_columns = [
        "wiki_movie_id",
        "freebase_movie_id",
        "name",
        "release_date",
        "box_office_revenue",
        "runtime",
        "languages",
        "countries",
        "genres",
    ]
    movies = pd.read_csv(movies_file, sep="\t", names=movies_columns)

    # clean dates
    movies["release_date"] = pd.to_datetime(
        movies["release_date"], format="%Y-%m-%d", errors="coerce"
    )

    return movies


def clean_unknowns(input_df, features=["countries", "genres", "languages"]):
    """
        Replace unkown values in countries, genres and languages
    """

    def replace_unknown(df, label):
        """
            Replace emtpy json with "Unknown"
        """
        return df[label].replace("{}", '{"": "Unknown"}')

    df = input_df.copy()

    for feature in features:
        df[feature] = replace_unknown(df, feature)

    return df


def clean_jsons(df_input, features=["countries", "genres", "languages"]):
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


def load_kaggle_movies(
    kaggle_file,
    columns=[
        "original_title",
        "revenue",
        "budget",
        "vote_average",
        "vote_count",
        "release_date",
    ],
):
    """
        TODO fill it
    """
    kaggle = pd.read_csv(kaggle_file, usecols=columns)

    # remove wrongly formatted rows (only 3)
    kaggle = kaggle.drop(kaggle[kaggle["budget"].str.contains(".jpg")].index)

    # convert date string to datetime objects
    kaggle["release_date"] = pd.to_datetime(
        kaggle["release_date"], format="%Y-%m-%d", errors="coerce"
    )

    # convert numerical columns to float
    kaggle["revenue"] = (
        kaggle["revenue"].astype(float).apply(lambda x: np.nan if x == 0.0 else x)
    )
    kaggle["budget"] = (
        kaggle["budget"].astype(float).apply(lambda x: np.nan if x == 0.0 else x)
    )

    return kaggle


def merge_characters_movies(characters, movies):
    """
        TODO fill it
    """
    # Movies and characters
    df = pd.merge(
        left=characters,
        right=movies,
        on="wiki_movie_id",
        how="left",
        suffixes=("_c", "_m"),
    )

    # clean features
    duplicate_columns = ["freebase_movie_id_c", "release_date"]
    df = df.drop(duplicate_columns, axis=1)
    df = df.rename(
        columns={
            "freebase_movie_id_m": "freebase_movie_id",
            "name_c": "char_name",
            "name_m": "movie_name",
            "m_release_date": "release_date",
        }
    )

    # change order of columns
    df = df[
        [
            "wiki_movie_id",
            "freebase_movie_id",
            "movie_name",
            "release_date",
            "box_office_revenue",
            "runtime",
            "genres",
            "languages",
            "countries",
            "char_name",
            "a_name",
            "a_gender",
            "a_ethnicity",
            "a_dob",
            "a_age_at_release",
            "a_height",
        ]
    ]

    return df


def merge_cmu_kaggle_movies(movies, kaggle):
    """
        TODO fill it
    """
    df = pd.merge(
        movies,
        kaggle,
        left_on=[movies["name"], movies["release_date"].dt.year],
        right_on=[kaggle["original_title"], kaggle["release_date"].dt.year],
        how="left",
    )
    df = df.rename({"release_date_x": "release_date"}, axis=1)

    # fill the box_office revenue with the kaggle revenue if it's missing
    df["box_office_revenue"] = df["box_office_revenue"].fillna(df["revenue"].copy())
    df = df.drop(
        columns=["revenue", "original_title", "key_0", "key_1", "release_date_y"]
    )

    return df


def load_inflation(inflation_file):
    """
        TODO fill it
    """

    inflation = pd.read_csv(inflation_file, index_col="year")
    inflation = inflation.rename(columns={"amount": "amount_1900"})

    reference_year = 2022
    inflation_reference_year = inflation.loc[reference_year, "amount_1900"]

    inflation["amount_2022"] = inflation["amount_1900"].apply(
        lambda x: inflation_reference_year / x
    )

    return inflation


def add_inflation_data(movies, inflation):
    def inflation_adjustment(row, column):
        if np.isnan(row[column]):
            return np.nan

        return row[column] * inflation.loc[row["release_date"].year, "amount_2022"]

    movies["box_office_inflation"] = movies.apply(
        lambda x: inflation_adjustment(x, "box_office_revenue"), axis=1
    )
    movies["budget_inflation"] = movies.apply(
        lambda x: inflation_adjustment(x, "budget"), axis=1
    )

    return movies


def add_missing_release_date(movies):
    missing_release_dates = {
        "The Impossible": "2008-07-18",
        "The Outing": "2001-01-01",
        "Into the Spider's Web": "2007-08-26",
        "Melissa P.": "2005-01-01",
        "The Lamp": "2000-01-01",
        "The Bear": "2000-01-01",
        "Meatballs III: Summer Job": "1987-01-01",
        "The Steel Trap": "2000-01-01",
        "Angels Die Hard": "2000-01-01",
        "American Cyborg: Steel Warrior": "1993-01-01",
        "Shattered Image": "1992-01-01",
        "The Ghost of Slumber Mountain": "2000-01-01",
        "Iron Warrior": "1989-01-01",
    }

    for movie_name, release_date in missing_release_dates.items():
        movies.loc[movies["name"] == movie_name, "release_date"] = pd.to_datetime(
            release_date
        )

    return movies


def add_gender_stats(df, movies):
    """
    
    """
    def compute_men_women_ratio(x):
        genders = x['a_gender']
        nb_actors = x['a_name'].count()
        nb_male = genders[genders == 'M'].count()
        nb_female = genders[genders == 'F'].count()
        nb_nan_gender = genders.isna().sum()

        nb_known_gender = nb_known_gender=nb_male+nb_female
        m_f_ratio = nb_male / nb_female if nb_female > 0 else 1 if nb_male > 0 else 0
        m_ratio = nb_male / nb_known_gender if nb_known_gender > 0 else 0
        f_ratio = nb_female / nb_known_gender  if nb_known_gender > 0 else 0
        nan_ratio = nb_nan_gender / x.shape[0]

        return pd.Series(index=['nb_actors', 'nb_male', 'nb_female', 'nb_nan_gender', 'm_ratio', 'f_ratio', 'M_F_ratio', 'nan_ratio'], data=[nb_actors, nb_male, nb_female, nb_nan_gender, m_ratio, f_ratio, m_f_ratio, nan_ratio])

    # compute stats
    df_gender = df.groupby('wiki_movie_id').apply(compute_men_women_ratio)

    df_gender['nb_actors'] = df_gender['nb_actors'].astype(int)
    df_gender['nb_male'] = df_gender['nb_male'].astype(int)
    df_gender['nb_female'] = df_gender['nb_female'].astype(int)
    df_gender['nb_nan_gender'] = df_gender['nb_nan_gender'].astype(int)

    return pd.merge(left=movies, right=df_gender, on='wiki_movie_id', how='left', suffixes=('_m', '_g'))


def add_ethnicities_ratio(df, movies):
    return ...


def add_age_height_weight_stats(df, movies):
    num_columns = ['a_age_at_release', 'a_height']

    movies_stats = df.groupby('wiki_movie_id')[num_columns].agg({
        'a_age_at_release': ['mean', 'std'], 
        'a_height': ['mean', 'std']
        })

    movies_stats.columns = ["_".join(col)for col in movies_stats.columns.to_flat_index()]

    return pd.merge(left=movies, right=movies_stats, on='wiki_movie_id', how='left', suffixes=('_m', '_s'))


def generate_clean_df(
    character_file,
    ethnicity_file,
    movies_file,
    kaggle_file,
    inflation_file,
    etchnicity_clusters,
    target_countries=["United States of America"],
):
    """
        TODO fill it
    """
    # characters
    characters = load_characters(character_file)
    ethnicities = load_ethnicities(ethnicity_file, etchnicity_clusters)
    characters = add_characters_ethnicities(characters, ethnicities)

    # movies
    cmu_movies = load_cmu_movies(movies_file)
    cmu_movies = clean_unknowns(cmu_movies)
    cmu_movies = clean_jsons(cmu_movies)

    # keep only U.S. movies
    cmu_movies = filter_with_countries(cmu_movies, target_countries, "any")

    # TODO: update this method to add something more clean
    add_missing_release_date(cmu_movies)

    # kaggle movies
    kaggle_movies = load_kaggle_movies(kaggle_file)

    # merge movies and kaggle movies
    movies = merge_cmu_kaggle_movies(cmu_movies, kaggle_movies)

    # inflation
    inflation = load_inflation(inflation_file)

    # add inflation data
    movies = add_inflation_data(movies, inflation)

    # merge movies and characters
    df = merge_characters_movies(characters, movies)

    return df


#
# DATA ANALYSIS
#


def filter_with_countries(df, target_countries, mode):
    """
        TODO fill it
    """
    # TODO drop na on every columns ?
    if mode == "all":
        return df[
            df["countries"].apply(
                lambda x: all(country in x for country in target_countries)
            )
        ]
    elif mode == "any":
        return df[
            df["countries"].apply(
                lambda x: any(country in x for country in target_countries)
            )
        ]
    elif mode == "only":
        return df[df["countries"].apply(lambda x: set(x) == set(target_countries))]
    else:
        raise ValueError("mode must be one of [all, any, only]")
