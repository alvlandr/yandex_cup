import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


FILEPATH = 'data.csv'

df = pd.read_csv(FILEPATH, header=None, names=['x', 'y'])
df['sinx'] = np.sin(df['x'])
df['lnx'] = np.log(df['x'])
df['x2'] = df['x'] ** 2

df['sinx2'] = df['sinx'] ** 2
df['lnx2'] = df['lnx'] ** 2
df['2_sinx_lnx'] = 2 * df['sinx'] * df['lnx']

model = LinearRegression()
X = df[['sinx2', 'lnx2', '2_sinx_lnx', 'x2']]

model.fit(X, df['y'])
print(r2_score(model.predict(X), df['y']))
