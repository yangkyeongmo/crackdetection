import cv2
import numpy as np
import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected", "-e",
        default=None,
        type=str)
    parser.add_argument(
        "--real", "-r",
        default=None,
        type=str)
    parser.add_argument(
        "--seg", "-s",
        type=int
    )
    parser.add_argument(
        "--dirname",
        type=str
    )
    return parser


def _get_area_comparison(expected_ovl, real_ovl, x, next_x, y, next_y, val_img):
    seg = next_x - x
    fp, fn = 0, 0
    core_x, core_y = x + seg//2, y + seg//2

    if all(expected_ovl[_y, _x][2] > 0 for _y in range(y, next_y) for _x in range(x, next_x)):
        if not any(real_ovl[_y, _x][2] > 0 for _y in range(y, next_y)
                   for _x in range(x, next_x)):
            val_img[y:next_y, x:next_x] = (255, 0, 0)
            fp = 1
    else:
        if any(real_ovl[_y, _x][2] > 0 for _y in range(core_y - 1, core_y + 1)
               for _x in range(core_x - 1, core_x + 1)):
            val_img[y:next_y, x:next_x] = (0, 255, 0)
            fn = 1
    return fp, fn


def _write_val_imgs(val_img, expected_ovl, real_ovl, path):
    bname = os.path.basename(path)
    cv2.imwrite(bname + "-validation.jpg", val_img)
    cv2.imwrite(bname + "-val_expected_ovl.jpg",
                cv2.addWeighted(expected_ovl, 0.5, val_img, 0.5, 0))
    cv2.imwrite(bname + "-val_real_ovl.jpg",
                cv2.addWeighted(real_ovl, 0.5, val_img, 0.5, 0))


def _iterate_through_imgs(expected_ovl, real_ovl):
    _rslt, _expected_count = 0, 0
    h, w = expected_ovl.shape[:2]

    val_img = np.zeros((h, w, 3), np.uint8)
    for x in range(0, w):
        for y in range(0, h):
            _rslt_n_expected = _get_pixel_comparison(expected_ovl, real_ovl,
                                                     x, y, val_img)
            _rslt, _expected_count = _rslt + _rslt_n_expected[0], \
                _expected_count + _rslt_n_expected[1]
    _write_val_imgs(val_img)
    return _rslt, _expected_count


def _iterate_through_imgs_areas(expected_ovl, real_ovl, seg, path):
    _rslt, _expected_count = 0, 0
    _fp, _fn = 0, 0
    h, w = expected_ovl.shape[:2]
    val_img = np.zeros((h, w, 3), np.uint8)
    x, next_x = 0, seg
    while next_x < w:
        y, next_y = 0, seg
        while next_y < h:
            _fp_n_fn = _get_area_comparison(expected_ovl, real_ovl,
                                                    x, next_x, y, next_y,
                                                    val_img)
            _fp, _fn = _fp + _fp_n_fn[0], _fn + _fp_n_fn[1]
            y, next_y = y + seg//3, next_y + seg//3
        x, next_x = x + seg//3, next_x + seg//3
    _write_val_imgs(val_img, expected_ovl, real_ovl, path)
    return _fp, _fn


def _get_image_comparison_result(expected_ovl_path, real_ovl_path, seg):
    _fp, _fn = 0, 0
    _expected_ovl = cv2.imread(expected_ovl_path)
    _real_ovl = cv2.imread(real_ovl_path)
    h, w = _expected_ovl.shape[:2]
    _res_real_ovl = cv2.resize(_real_ovl, (w, h))
    _fp, _fn = _iterate_through_imgs_areas(_expected_ovl, _res_real_ovl, seg, expected_ovl_path)
    print("TARGET : " + os.path.basename(expected_ovl_path))
    print("FP : " + _fp.__str__())
    print("FN : " + _fn.__str__())

    return _fp, _fn


def iterate_through_folder(arg):
    parent = os.path.abspath(arg.dirname) + '\\'
    #get "base.jpg"
    parent_f_list = os.listdir(parent)
    base = parent + [s for s in parent_f_list if 'base.jpg' in s][0]
    for parent_f in parent_f_list:
        full_path = os.path.join(parent, parent_f)
        if os.path.isdir(full_path):
            seg = parent_f
            for f in os.listdir(full_path):
                main(os.path.join(full_path, f), base, int(seg))



def dir_main(arg):
    f_list = os.listdir(arg.dirname)
    real = [s for s in f_list if 'base.jpg' in s][0]
    for f in f_list:
        expected_path = os.path.abspath(arg.dirname + f)
        real_path = os.path.abspath(arg.dirname + real)
        print(real_path)
        main(expected_path, real_path, arg.seg)


def main(expected_path, real_path, seg):
    if not os.path.isfile(expected_path) or not os.path.isfile(
            real_path):
        print("NOT FILE ERROR: " + expected_path + "\n" + real_path)
        return
    fp, fn = _get_image_comparison_result(expected_path, real_path, seg)
    '''print("Comparison of " + os.path.basename(expected_path) + " & " +
        os.path.basename(real_path) + " is: " + rslt.__str__())
    '''
    f = open("comparison_output.txt", 'a')
    f.write(os.path.basename(expected_path) + '\nFP : ' + fp.__str__()
        + '\nFN : ' + fn.__str__() + '\n')
    f.close()


def entry():
    parser = get_parser()
    arg = parser.parse_args()
    iterate_through_folder(arg)
    return
    if arg.dirname is None or os.path.isfile(arg.dirname):
        expected_path = os.path.abspath(arg.expected)
        real_path = os.path.abspath(arg.real)
        main(expected_path, real_path, arg.seg)
    elif os.path.isdir(arg.dirname):
        dir_main(arg)
    else:
        print("ERROR")


if __name__ == "__main__":
    entry()
