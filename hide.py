# %%
import os
import pandas as pd

# %%
files = pd.read_json('suspects.json')
files

# %%


def new_path(path):
    return f'{path}'
    # return f'{path}_customized'


for j in files.index:
    se = files.loc[j]
    path = os.path.join(se.Folder, se.Name)
    print(path)

    try:
        os.rename(path, new_path(path))
    except FileNotFoundError:
        pass


# %%
