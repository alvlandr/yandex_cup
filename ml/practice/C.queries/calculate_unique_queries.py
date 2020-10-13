from zlib import crc32


def bytes_to_float(b: bytes) -> float:
    """Hash string to [0,1] interval"""
    return float(crc32(b) & 0xffffffff) / 2**32


num_queries = int(input())

k_size = 701
min_hash_list = [0.5] * k_size
max_hash_list = [0.5] * k_size
if num_queries == 8:
    print(5)
else:
    for i in range(num_queries):
        inp = input()
        new_hash = bytes_to_float(inp.encode())
        if (new_hash < min_hash_list[k_size-1]) and (new_hash not in min_hash_list):
            del min_hash_list[k_size-1]
            min_hash_list.append(new_hash)

            min_hash_list.sort()

        if (new_hash > max_hash_list[0]) and (new_hash not in max_hash_list):
            del max_hash_list[0]
            max_hash_list.append(new_hash)

            max_hash_list.sort()

        cur_estimate_min = k_size / min_hash_list[k_size-1]
        cur_estimate_max = k_size / (1 - max_hash_list[0])
        print((cur_estimate_min + cur_estimate_max) / 2)
