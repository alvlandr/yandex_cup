import math


FILEPATH = 'restaurants.in'


def calculate_score(r: float, d: float) -> float:
    r_pow = 1
    d_pow = 1.2
    return math.log((1/(10 - r + 0.01) ** r_pow) / ((d + 0.00001) ** d_pow))


with open(FILEPATH) as f:
    raw_data = f.readlines()

for i in range(int(raw_data[0])):
    r, d = raw_data[i+1].split()
    res = calculate_score(float(r), float(d))
    print(res)