import cv2
import numpy as np
import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
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
