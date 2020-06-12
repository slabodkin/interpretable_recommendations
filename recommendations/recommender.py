import os
import pandas as pd
from items.models import Movie

RATES_DATA_DIR = "./utils/"

def recommend_for_user(email, rates_csv=os.path.join(RATES_DATA_DIR, "rates.csv")):
    rate_df = pd.read_csv(rates_csv)
    items_seen_by_user = set(rate_df[rate_df.user == email].item)
    items_not_seen_by_user = rate_df[~rate_df.item.isin(items_seen_by_user)].item
    if items_not_seen_by_user.shape[0] > 0:
        return list(items_not_seen_by_user)
    return ""