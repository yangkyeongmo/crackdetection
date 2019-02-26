import sys
import math


def add_0_by_cipher(num, max_c):
    str_num = str(num)
    comp = 10**(max_c - 1)
    while comp >= 1:
        mult = max_c - int(math.log10(comp) + 1)
        if comp <= num < comp*10:
            str_num = '0'*mult + str_num
            break
        comp /= 10
    if num == 0:
        str_num = '0'*max_c
    return str_num


if __name__ == "__main__":
    print(add_0_by_cipher(int(sys.argv[1]), int(sys.argv[2])))
