import pandas as pd

df_player_data = pd.read_pickle("simulator/data/player_data")
print(df_player_data["club"].unique())
