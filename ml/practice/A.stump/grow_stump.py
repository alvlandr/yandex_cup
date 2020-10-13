STOP_THRESHOLD = 1e-3


def l2_loss(y_pred: int, y_true: int) -> float:
    return (y_pred - y_true) ** 2


def list_mean(clist: list) -> float:
    return sum(clist) / len(clist)


def update_left_mean(prev_mean: float, upd_list: list, prev_len: int) -> float:
    adj_mean = (prev_len / (prev_len + len(upd_list))) * prev_mean
    adj_value = sum(upd_list) / (prev_len + len(upd_list))
    return adj_mean + adj_value


def update_right_mean(prev_mean: float, upd_list: list, prev_len: int) -> float:
    adj_mean = (prev_len / (prev_len - len(upd_list))) * prev_mean
    adj_value = sum(upd_list) / (prev_len - len(upd_list))
    return adj_mean - adj_value


with open('stump.in') as f:
    objs = [tuple(map(float, line.split())) for line in f]
num_pairs = objs[0][0]
objs = objs[1:]

objs.sort(key=lambda x: x[0])
xs, ys = zip(*objs)

l_edges = [xs.index(i) for i in set(xs)]
l_edges.sort()

left_child = []
right_child = ys[:]
l_mean = 0
data_mean = list_mean(right_child)
r_mean = data_mean

a, b, c = l_mean, r_mean, xs[0]
params = [(a, b, c, abs(b-a), 0)]
loss = (sum([l2_loss(b, i) for i in right_child]) / len(right_child)) ** 0.5
if loss > STOP_THRESHOLD:
    for idx, l_edge in enumerate(l_edges[1:], 1):
        left_branch = ys[:l_edge]
        right_branch = ys[l_edge:]

        c_new = (xs[l_edges[idx]] + xs[l_edges[idx]-1]) / 2
        upd_list = ys[l_edges[idx - 1]:l_edges[idx]]

        prev_l_mean, prev_r_mean = l_mean, r_mean
        l_mean = update_left_mean(l_mean, upd_list, l_edges[idx-1])
        r_mean = update_right_mean(r_mean, upd_list, len(ys) - l_edges[idx-1])

        params.append(
            (
                l_mean,
                r_mean,
                c_new,
                abs(l_mean - data_mean) + abs(r_mean - data_mean),
                idx,
            ),
        )

    params.sort(key=lambda x: -x[3])

    for p in params:
        left_branch = ys[:l_edges[p[4]]]
        right_branch = ys[l_edges[p[4]]:]

        left_loss = sum([l2_loss(p[0], i) for i in left_branch])
        right_loss = sum([l2_loss(p[1], i) for i in right_branch])

        lr_loss = left_loss + right_loss
        new_loss = (lr_loss / (len(left_branch) + len(right_branch))) ** 0.5

        if new_loss < loss:
            loss = new_loss
            a, b, c = p[0], p[1], p[2]
        if new_loss <= STOP_THRESHOLD:
            break

print(f'{a:f} {b:f} {c:f}')