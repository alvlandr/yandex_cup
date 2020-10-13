import os

import pandas as pd


MODE = 'open_task'  # either open_task or hidden_task
QID_FILENAME = 'qid_query.tsv'
HOST_FILENAME = 'hostid_url.tsv'
RATING_FILENAME = 'qid_url_rating.tsv'


def calculate_pfound(rel: list, pbreak: float=0.15) -> float:
    plook = [0] * 10
    plook[0] = 1
    pfound = plook[0] * rel[0]

    for i in range(1, 10):
        plook[i] = plook[i-1] * (1 - rel[i-1]) * (1 - pbreak)
        pfound += plook[i] * rel[i]

    return pfound


qids = pd.read_csv(
    os.path.join(MODE, QID_FILENAME),
    sep='\t',
    header=None,
    names=['qid', 'query'],
)
hosts = pd.read_csv(
    os.path.join(MODE, HOST_FILENAME),
    sep='\t',
    header=None,
    names=['hid', 'url'],
)
ratings = pd.read_csv(
    os.path.join(MODE, RATING_FILENAME),
    sep='\t',
    header=None,
    names=['qid', 'url', 'rating'],
)

ratings = pd.merge(ratings, hosts, how='left', on='url')
ratings_cleaned = ratings.groupby(['qid', 'hid'])['rating'].nlargest(1)
ratings_cleaned = ratings_cleaned.reset_index()
ratings_cleaned = ratings_cleaned.groupby('qid')['rating'].nlargest(10)
ratings_cleaned = ratings_cleaned.reset_index()

pfound_list = []
qids_list = ratings_cleaned['qid'].unique().tolist()
for q in qids_list:
    rel = ratings_cleaned.loc[
        ratings_cleaned['qid'] == q,
        'rating',
    ].values.tolist()
    rel.sort(reverse=True)
    pfound = calculate_pfound(rel)

    pfound_list.append(pfound)

qid_max_pfound = qids_list[pfound_list.index(max(pfound_list))]
print(qids[qids['qid'] == qid_max_pfound])
