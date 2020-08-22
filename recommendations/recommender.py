import pandas as pd 
import numpy as np
import scipy.sparse
import sklearn.preprocessing

import os


# RATES_DATA_DIR = "./utils/"
DATA_DIR = "./data/"

def recommend_for_user_non_seen(user_id, rates_csv=os.path.join(DATA_DIR, "example_rates.csv")):
    rate_df = pd.read_csv(rates_csv)
    items_seen_by_user = set(rate_df[rate_df["user"] == user_id].item)
    items_not_seen_by_user = rate_df[~rate_df.item.isin(items_seen_by_user)].item
    if items_not_seen_by_user.shape[0] > 0:
        return list(items_not_seen_by_user)
    return ""

# set all rates to 1 (we are interested if the user read the given book, not in how they rated it)
# compute cosine between the user's books and all other ones
# for each book compute the maximum cosine similatiry among the user's books 
# sort books by this similarity
def recommend_for_user(user_id, n_items_to_recommend=10, rates_df=None):
    if rates_df is None:
        rates_df = pd.read_csv(os.path.join(DATA_DIR, 'rates_imhonet.csv'), sep=',')
        rates_df = rates_df.drop("Unnamed: 0", axis=1)
    rates_df["rate"] = 1

    user_type = pd.api.types.CategoricalDtype(np.sort(rates_df.user_id.unique()), ordered=True)
    item_type = pd.api.types.CategoricalDtype(np.sort(rates_df.element_id.unique()), ordered=True)

    row_inds = rates_df.user_id.astype(user_type).cat.codes
    col_inds = rates_df.element_id.astype(item_type).cat.codes
    sparse_rate_matrix = scipy.sparse.csc_matrix((rates_df.rate, (row_inds, col_inds)),
                                            shape=(user_type.categories.size,
                                                   item_type.categories.size))
    #normalize for cos computation
    sparse_rate_matrix = sklearn.preprocessing.normalize(sparse_rate_matrix, norm="l2", axis=0)

    user_row_ind = user_type.categories.get_loc(user_id)
    user_row = sparse_rate_matrix[user_row_ind, :]
    user_item_col_inds = user_row.nonzero()[1]
    user_item_ids = item_type.categories[user_item_col_inds]
    user_item_ids

    user_items_submatrix = sparse_rate_matrix[:, user_item_col_inds]
    cosine_values = sparse_rate_matrix.T.dot(user_items_submatrix).todense()
    best_cosine_values = np.asarray(cosine_values.max(axis=1)).reshape(-1,)


#     n_items_to_recommend = 10

    top_items = np.argsort(best_cosine_values)[::-1]
    #filter books already read by user 
    top_items = top_items[~np.isin(top_items, user_item_col_inds)][:n_items_to_recommend]
    return list(item_type.categories[top_items])



def build_table(user_id_list, n_items_to_recommend=10, rates_df=None):
    # запускаем рекомендацию для каждого юзера из списка юзеров
    # пишем в таблицу, когда все записались
    built_recommendations = {}
    recommended_pairs = {}
    for i in user_id_list: 
        built_recommendations[i] = recommend_for_user(i)
    for key in built_recommendations:
        for i in built_recommendations[key]:
            recommended_pairs[key] = i
    df = pd.DataFrame(recommended_pairs, columns= ['user_id', 'item_id'])
    df.to_csv (os.path.join(DATA_DIR, 'precalculated_recommendations.csv'), index = False, header=True)

def fetch_values(user_id):
    data = pd.read_csv(os.path.join(DATA_DIR, 'precalculated_recommendations.csv'))
    rslt_df = dataframe[dataframe['user_id'] == user_id]
    return list(rslt_df['item_id'])

