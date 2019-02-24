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
        "--record",
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
        if any(real_ovl[_y, _x][2] > 0 for _y in range(core_y - 1, core_y + 1)\
               for _x in range(core_x - 1, core_x + 1)):
            val_img[y:next_y, x:next_x] = (0, 255, 0)
            fn = 1
    return fp, fn


def _write_val_imgs(val_img, expected_ovl, real_ovl, expected_ovl_path):
    parent_path = os.path.dirname(expected_ovl_path)
    val_dir = os.path.join(parent_path, "VAL")
    if not os.path.exists(val_dir):
        os.mkdir(val_dir)
    filebasename = os.path.basename(expected_ovl_path)
    cv2.imwrite(os.path.join(val_dir,
                filebasename + "-validation.jpg"), val_img)
    cv2.imwrite(os.path.join(val_dir,
                filebasename + "-val_expected_ovl.jpg"),
                cv2.addWeighted(expected_ovl, 0.5, val_img, 0.5, 0))
    cv2.imwrite(os.path.join(val_dir,
                filebasename + "-val_real_ovl.jpg"),
                cv2.addWeighted(real_ovl, 0.5, val_img, 0.5, 0))


def _iterate_through_imgs_areas(expected_ovl_path, real_ovl_path, seg):
    _fp, _fn = 0, 0
    expected_ovl = cv2.imread(expected_ovl_path)
    h, w = expected_ovl.shape[:2]
    real_ovl = cv2.imread(real_ovl_path)
    res_real_ovl = cv2.resize(real_ovl, (w, h))
    val_img = np.zeros((h, w, 3), np.uint8)
    x, next_x = 0, seg
    while next_x < w:
        y, next_y = 0, seg
        while next_y < h:
            _fp_n_fn = _get_area_comparison(expected_ovl, res_real_ovl,
                                            x, next_x, y, next_y,
                                            val_img)
            _fp, _fn = _fp + _fp_n_fn[0], _fn + _fp_n_fn[1]
            y, next_y = y + seg//3, next_y + seg//3
        x, next_x = x + seg//3, next_x + seg//3
    _write_val_imgs(val_img, expected_ovl, res_real_ovl, expected_ovl_path)
    return _fp, _fn


def _get_image_comparison_result(expected_ovl_path, real_ovl_path, seg):
    _fp, _fn = 0, 0
    _fp, _fn = _iterate_through_imgs_areas(expected_ovl_path, real_ovl_path, seg)
    print("TARGET : " + os.path.basename(expected_ovl_path))
    print("FP : " + _fp.__str__())
    print("FN : " + _fn.__str__())
    return _fp, _fn


def get_path_is_not_file(expected_ovl_path, real_ovl_path):
    if not os.path.isfile(expected_ovl_path) or\
        not os.path.isfile(real_ovl_path):
        print("NOT FILE ERROR: " + expected_ovl_path + "\n" + real_ovl_path)
        return True
    return False


def main():
    parser = get_parser()
    arg = parser.parse_args()
    if get_path_is_not_file(arg.expected, arg.real):
        return
    fp, fn = _get_image_comparison_result(expected_ovl_path=arg.expected,
                                          real_ovl_path=arg.real,
                                          seg=arg.seg)
    f = open(arg.record + "/comparison_output.txt", 'a')
    f.write(os.path.basename(arg.expected) + '\nFP : ' + fp.__str__()
            + '\nFN : ' + fn.__str__() + '\n')
    f.close()


if __name__ == "__main__":
    main()
