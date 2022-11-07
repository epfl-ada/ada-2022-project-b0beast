import pandas as pd
import numpy as np
import requests

# input
DATA_FOLDER = './data/'
MOVIES_FOLDER = DATA_FOLDER + 'movies_summaries/'
CHARACTERS_FILE = MOVIES_FOLDER + 'character.metadata.tsv'

# output
ETHNICITY_FILE = './gen/ethnicities.txt'

# import characters dataset
character_columns = ['wiki_movie_id', 'freebase_movie_id', 'm_release_date', 'name', 'a_dob', 'a_gender', 'a_height', 'a_ethnicity_freebase_id', 'a_name', 'a_age_at_release', 'freebase_char/a_map', 'freebase_char_id', 'freebase_a_id']
characters = pd.read_csv(CHARACTERS_FILE, sep='\t', names=character_columns, index_col=False)

def get_ethnicities(ethnicities_id):    
    """
        Recover ethnicity names from freebase id's using sparql query

        :enthicities_id: list of freebase id's
    """
    url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"

    query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wikibase: <http://wikiba.se/ontology#>

        SELECT  ?s ?sLabel ?p  ?o ?oLabel WHERE {{
            {}

            SERVICE wikibase:label {{
                bd:serviceParam wikibase:language "en" .
            }}
        }}
    '''

    # add every id in UNION
    ethnicities_id = ethnicities_id.apply(lambda x: '{{?s wdt:P646 "{}"}}'.format(x))
    ethnicities_id.iloc[1:] = ethnicities_id.iloc[1:].apply(lambda x: ' UNION ' + x)

    query = query.format(ethnicities_id.str.cat())
    response = requests.get(url, params = {'format': 'json', 'query': query})
    return response

# get all unique ethnicity id's
ethnicities_id = pd.Series(characters['a_ethnicity_freebase_id'].unique())
ethnicities_id = ethnicities_id.iloc[1:] # remove nan

# We cannot query all id's at once. We need to split the query in multiple requests.
ethnicities = []
idx_ranges = np.linspace(0, ethnicities_id.size, 5, dtype=int)

for i in range(1, len(idx_ranges)):
    idx_range = np.arange(idx_ranges[i-1], idx_ranges[i])
    response = get_ethnicities(ethnicities_id.iloc[idx_range])

    # add all results to the list
    results = response.json()
    for res in results['results']['bindings']:
        ethnicities.append(res['sLabel']['value'])

# values which don't have information
undefined_values = ['Q31340083', 'Q97377726', 'Q54864438', 'Q56408633', 'Q25467191']

with open(ETHNICITY_FILE, 'w', encoding='utf-8') as f:
    for ethnicity in ethnicities:
        if ethnicity not in undefined_values:
            f.write("{}\n".format(ethnicity))

print("Data generated in {}".format(ETHNICITY_FILE))