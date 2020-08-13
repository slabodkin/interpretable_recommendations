import pandas as pd 
import numpy as np
import os
import csv
from itertools import islice
import random
import string

DATA_DIR = "./data/"

OUTPUT_FILE = os.path.join(DATA_DIR, 'generated_users_imhonet.csv')

rates_df = pd.read_csv(os.path.join(DATA_DIR, 'rates_imhonet.csv'), sep=',')
rates_df = rates_df.drop("Unnamed: 0", axis=1)

with open(os.path.join(DATA_DIR, 'names_list.txt')) as name_file:
    head = list(islice(name_file, 5))
names = []
for i in head:
    names.append(i.strip())
number_of_users = 10
# taking a subset of user_ids
list_of_names = np.random.choice(names, size=number_of_users, replace=True) # random.sample(names, 10)

emails = []
emails_set = set()
for i in list_of_names:
    #print(i)
    k = ''
    while (i + str(k)) in emails_set:
        k = random.randint(1,101)
    emails_set.add(i + str(k))
    emails.append(i + str(k) +  '@andrec.no')

# generating passwords
def random_string(string_length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))

passwords = []    
password_length = 8
for i in range(len(list_of_names)):
    k = random_string(password_length)
    passwords.append(k)

users_ids_for_csv = rates_df['user_id'].tolist()
users_ids_for_csv = users_ids_for_csv[:number_of_users]
rows = zip(users_ids_for_csv, list_of_names, emails, passwords)

    
    
with open(OUTPUT_FILE, "w") as otp:
    writer = csv.writer(otp)
    otp.write("user_id,email,password,name")
    for row in rows:
        writer.writerow(row)