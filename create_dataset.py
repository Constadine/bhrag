import pandas as pd
import os 

folder_path = os.path.join(os.getcwd(), 'perfumes', 'list_of_perfumes')
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
df_list = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df_list.append(pd.read_csv(file_path))
df = pd.concat(df_list, ignore_index=True)

concepts = []
for concept_list in df['concepts'].values:
    concepts.extend(eval(concept_list))

unique_concepts = list(set(concepts))
unique_concepts_df = pd.DataFrame({concept: [0]*len(df) for concept in unique_concepts})

for i in range(len(df)):
    for concept in eval(df.iloc[i]['concepts']):
        unique_concepts_df.loc[i, concept] = 1
unique_concepts_df.fillna(0, inplace=True)

df = pd.concat([df, unique_concepts_df], axis=1)
df = df.iloc[:, -98:]

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
def get_top_n_similar(row, n=3):
    sims = cosine_similarity([row], df.iloc[:, -98:]).flatten()
    sims = sims[sims != 1] # remove self similarity
    idx = np.argsort(sims)[-n:]
    return pd.DataFrame({'similar': df.iloc[idx, 0], 'similarity': sims[idx]})
