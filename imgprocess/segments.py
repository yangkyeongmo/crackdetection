import cv2
import os
import argparse
import math


def get_file_list(path):
    filelist = list()
    if not os.path.exists(path):
        print("NO SUCH PATH ERROR:", path)
        return
    if not os.path.isfile(path):
        if not os.path.isdir(path):
            print("NOT FILE NOR DIR ERROR:", path)
            return
        else:
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if os.path.isfile(filepath):
                    filelist.append(filepath)
    else:
        filelist.append(path)
        if not path[-4:] == '.jpg':
            print("NOT IMAGE ERROR:", path)
            return
    return filelist


def get_segdir(path, dest):
    if dest != "":
        if not os.path.exists(dest):
            os.mkdir(dest)
        dir = dest
    else:
        dir = os.path.dirname(path)
    return dir


def create_seg(path, segdir, intv, move):
    max_length = 800
    max_cipher = int(math.log10(max_length))
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = resize_img_by_max_length(max_length, img)
    h, w = img.shape[:2]
    x, y = 0, 0
    next_x, next_y = x+intv, y+intv
    # 정사각형을 형성하지 못하면 가져오지 않음
    while next_x < w:
        while next_y < h:
            # normalilze x, y string
            str_x = add_0_by_cipher(x, max_cipher)
            str_y = add_0_by_cipher(y, max_cipher)
            write_path = get_write_path(segdir, str_x, str_y)
            print(write_path)
            trimed = img[y:next_y, x:next_x]
            cv2.imwrite(write_path, trimed)
            y = y + move
            next_y += move
        x = x + move
        next_x += move
        y = 0
        next_y = y + intv


def resize_img_by_max_length(max_length, img):
    h, w = img.shape[:2]
    if h > w:
        w = w*max_length//h
        h = max_length
    else:
        w = max_length
        h = h*max_length//w
    return cv2.resize(img, (w, h))


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


def get_write_path(segdir, str_x, str_y):
    original_write_path = os.path.join(segdir, str_x + str_y)
    write_path = original_write_path
    i = 0
    while os.path.exists(write_path + '.jpg'):
        write_path = original_write_path + '(' + str(i) + ')'
        i = i + 1
    return write_path + '.jpg'


def main(path, intv, dest, move):
    filelist = get_file_list(path)
    segdir = get_segdir(path, dest)
    for filepath in filelist:
        create_seg(filepath, segdir, intv, move)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("--intv", type=int)
    parser.add_argument("--dest")
    parser.add_argument("--move", default=10, type=int)
    arg = parser.parse_args()
    main(arg.path, arg.intv, arg.dest, arg.move)
