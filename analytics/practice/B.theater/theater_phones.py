import pandas as pd


FILEPATH = 'ticket_logs.csv'

df = pd.read_csv(FILEPATH, header=None, names=['play', 'number'])
df['clean_number'] = df['number'].replace({'[-,.+\(\)]': ''}, regex=True)
print(df.groupby('play')['clean_number'].nunique().nlargest(1))
