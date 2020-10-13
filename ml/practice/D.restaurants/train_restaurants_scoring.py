import pandas as pd
import numpy as np
import math


FILEPATH = 'restaurants_train.txt'


def labeler(arr):
    return np.array([0 if i < 0 else 1 for i in arr])


def metric(score_looser: float, score_winner: float):
    return np.log(1 + np.exp(score_looser-score_winner))


def score_function(df: pd.DataFrame, r_col: str, d_col: str,
                    r_pow: float, d_pow: float) -> float:
    r_part = (1 / (10 - df[r_col] + 0.01) ** r_pow)
    d_part = ((df[d_col] + 0.00001) ** d_pow)

    return np.log(r_part / d_part)


df = pd.read_csv(FILEPATH, sep='\t', header=None, names=['winner', 'r1', 'r2', 'd1', 'd2'])
res_list = []
for r_pow in np.arange(1, 5, 0.1):
    for d_pow in np.arange(0.1, 1.5, 0.1):
        df['rd1'] = score_function(df, 'r1', 'd1', r_pow, d_pow)
        df['rd2'] = score_function(df, 'r2', 'd2', r_pow, d_pow)

        df_short = df[df['r1'] > 0]
        df_short = df_short[df_short['r2'] > 0]
        df_short = df_short[df_short['winner'] != 0.5]
        df_short['res'] = labeler(df_short['rd2'].values-df_short['rd1'].values)

        df.loc[df['winner'] == 1, 'metric'] = list(
            map(
                lambda x: metric(x[0], x[1]),
                df.loc[df['winner'] == 1, ['rd1', 'rd2']].values.tolist(),
            ),
        )
        df.loc[df['winner'] < 1, 'metric'] = list(
            map(
                lambda x: metric(x[1], x[0]),
                df.loc[df['winner'] < 1, ['rd1', 'rd2']].values.tolist(),
            ),
        )

        quality = df['metric'].mean()
        res_list.append((r_pow, d_pow, quality))

res_list.sort(key=lambda x: x[2])
r_pow, d_pow, quality = res_list[0]

df['rd1'] = score_function(df, 'r1', 'd1', r_pow, d_pow)
df['rd2'] = score_function(df, 'r2', 'd2', r_pow, d_pow)
df.loc[df['winner'] == 1, 'metric'] = list(
    map(
        lambda x: metric(x[0], x[1]),
        df.loc[df['winner'] == 1, ['rd1', 'rd2']].values.tolist(),
    ),
)
df.loc[df['winner'] < 1, 'metric'] = list(
    map(
        lambda x: metric(x[1], x[0]),
        df.loc[df['winner'] < 1, ['rd1', 'rd2']].values.tolist(),
    ),
)

print(f'''{r_pow:.2f}, {d_pow:.2f}, {quality:.2f}''')
print(df['metric'].mean())