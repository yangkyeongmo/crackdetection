import cv2
import numpy as np
import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
<<<<<<< HEAD
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
=======
        "--compare1", "-c1",
        default=None,
        type=str)
    parser.add_argument(
        "--compare2", "-c2",
        default=None,
        type=str)
    parser.add_argument(
        "--seg",
        default=None,
        type=int)

    return parser


def _get_img_part(img, x, next_x, y, next_y):
    return img[y:next_y, x:next_x]


def _get_avg(img):
    return img.mean(axis=0).mean(axis=0)


def _get_partial_comparison_result(img1, img2, x, next_x, y, next_y):
    _partial_result = 0
    _red_count = 0
    _img1_part = _get_img_part(img1, x, next_x, y, next_y)
    _img2_part = _get_img_part(img2, x, next_x, y, next_y)
    _img1_avg = _get_avg(_img1_part)
    _img2_avg = _get_avg(_img2_part)
    print("img1 avg: " + _img1_avg.__str__() + '\n' +
          "img2 avg: " + _img2_avg.__str__() + '\n' +
          "img position: " + x.__str__() + ", " + y.__str__())
    if _img2_avg[2] > 113:
        _partial_result = 1
        if _img1_avg[2] > 0:
            _red_count = 1
    return _partial_result, _red_count


def _iterate_through_imgs(img1, img2, seg):
    _rslt, _red_count = 0, 0
    h, w = img1.shape[:2]
    x, next_x = 0, seg

    val_img = np.zeros((h, w, 3), np.uint8)
    while x < w:
        y, next_y = 0, seg
        while y < h:
            _p_rslt, _p_r_count = _get_partial_comparison_result(
                    img1, img2, x, next_x, y, next_y)
            _rslt += _p_rslt
            _red_count += _p_r_count
            if _p_r_count == 1:
                val_img[y:next_y, x:next_x] = (0, 0, 255)
            y += seg//3
            next_y += seg//3
            if next_y > h:
                next_y = h
        x += seg//3
        next_x += seg//3
        if next_x > w:
            next_x = w
    cv2.imwrite("validation.jpg", val_img)
    cv2.imwrite("val_img1.jpg",
                cv2.addWeighted(img1, 0.5, val_img, 0.5, 0))
    cv2.imwrite("val_img2.jpg",
                cv2.addWeighted(img2, 0.5, val_img, 0.5, 0))
    return _rslt, _red_count


def _get_image_comparison_result(img1_path, img2_path, seg):
    _rslt = 0
    _red_count = 0
    _img1 = cv2.imread(img1_path)
    _img2 = cv2.imread(img2_path)
    h, w = _img2.shape[:2]
    _res_img1 = cv2.resize(_img1, (w, h))
    _rslt, _red_count = _iterate_through_imgs(_res_img1, _img2, seg)

    if _rslt != 0:
        tp = _red_count / _rslt
    else:
        tp = 'INF'
    return tp


def main():
    parser = get_parser()
    arg = parser.parse_args()
    path1 = os.path.abspath(arg.compare1)
    path2 = os.path.abspath(arg.compare2)
    try:
        if not os.path.isfile(path1) or not os.path.isfile(
                path2):
            raise Exception
        rslt = _get_image_comparison_result(arg.compare1, arg.compare2,
                                            arg.seg)
        print("Comparison of " + os.path.basename(path1) + " & " +
              os.path.basename(path2) + " is: " + rslt.__str__())
        f = open("comparison_output.txt", 'a')
        f.write(os.path.basename(path1) + " & " +
                os.path.basename(path2) + " = " + rslt.__str__() + '\n')
        f.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
>>>>>>> 910834ac7aa4d921b9e1311d77232b1a5a6e5eea
