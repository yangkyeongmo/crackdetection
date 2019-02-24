import cv2
import argparse


def draw_subline(img, i, seg, do_x):
    _img = img
    h, w = img.shape[:2]
    _THICKNESS = 1
    for j in range(1, 3):
        pos = i*seg + j*seg//3
        if do_x:
            _img = cv2.line(img, (pos, 0), (pos, h), _THICKNESS)
        else:
            _img = cv2.line(img, (0, pos), (w, pos), _THICKNESS)
    return _img


def draw_line_iterate(img, arg, do_x):
    h, w = img.shape[:2]
    target = w
    seg = arg.seg
    THICKNESS = 20
    if not do_x:
        target = h
    for i in range(0, target//seg):
        if i*seg < target:
            if do_x:
                vec1, vec2 = (i*seg, 0), (i*seg, h)
            else:
                vec1, vec2 = (0, i*seg), (w, i*seg)
            img = cv2.line(img, vec1, vec2, THICKNESS)
            if arg.draw_subgrid:
                img = draw_subline(img, i, seg, do_x)
    return img


def draw_line(img, arg):
    h, w = img.shape[:2]
    img = draw_line_iterate(img, arg, True)
    img = draw_line_iterate(img, arg, False)
    return img


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "img",
        default=None,
        type=str)
    parser.add_argument(
        "seg",
        default=None,
        type=int)
    parser.add_argument(
        "--draw_subgrid",
        default=True,
        action="store_false")
    return parser


def main():
    parser = get_parser()
    arg = parser.parse_args()
    img = cv2.imread(arg.img)
    mod_img = draw_line(img, arg)
    cv2.imwrite(arg.img + '-grid.jpg', mod_img)


if __name__ == "__main__":
    main()
