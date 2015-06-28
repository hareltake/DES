import random

from Box import s
from Util import to_binary


LINEAR_EXAMPLE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
RANDOM_EXAMPLE = [15, 7, 4, 6, 12, 10, 3, 15, 4, 9, 2, 12, 2, 13, 11, 6, 4, 10, 15, 0, 4, 8, 13, 13, 3, 15, 8, 5, 0, 5, 15, 13, 9, 14, 8, 2, 9, 12, 1, 13, 8, 3, 3, 4, 9, 13, 0, 11, 5, 0, 15, 0, 2, 0, 13, 15, 5, 12, 11, 10, 4, 4, 2, 11]


def linear_s_box():
    s_box = [[0 for col in range(16)] for row in range(4)]
    bin = []
    for i in range(64):
        bin = to_binary(i)
        s_box[bin[2] * 2 + b[7]][b[3] * 8 + b[4] * 4 + b[5] * 2 + b[6]] = b[3] * 8 + b[4] * 4 + b[5] * 2 + b[6]

def random_example():
    s_box = [[0 for col in range(16)] for row in range(4)]
    for i in range(64):
        s_box[i / 16][i % 16] = random.randint(0, 15)

def non_linear_s_box():
    s_box = []
    for i in range(64):
        s_box.append(0)
    for i in range(64):
        b = to_binary(i)
        s_box[(b[2] * 2 + b[7]) * 16 + b[3] * 8 + b[4] * 4 + b[5] * 2 + b[6]] = b[3] ** 4 + b[4] ** 3 + b[5] ** 2 + b[6]
    return s_box

def do_s_box(index, _s_box):
    b = [0] * 6
    n = index
    for i in range(6):
        b[5 - i] = n % 2
        n /= 2
    return _s_box[(b[0] * 2 + b[5]) * 16 + b[1] * 8 + b[2] * 4 + b[3] * 2 + b[4]]


def calculate_diff(_s_box):
    diff_table = [[0 for col in range(16)] for row in range(64)]
    for i in range(64):
        for j in range(64):
            in_diff = i ^ j
            out_diff = do_s_box(i, _s_box) ^ do_s_box(j, _s_box)
            diff_table[in_diff][out_diff] += 1
    return diff_table

def main():
    #NON_LINEAR_EXAMPLE = non_linear_s_box()
    diff_table = calculate_diff(RANDOM_EXAMPLE)
    for i in range(0, len(diff_table), 2):
        print str((i, diff_table[i])) + '   ' + str((i+1, diff_table[i+1]))

if __name__ == '__main__':
    main()