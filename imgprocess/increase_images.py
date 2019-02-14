import cv2
import argparse
import os


def increase_img(path, arg):
    imgname = path[:-4]
    img = cv2.imread(path)
    if not arg.all:
        return
    if not arg.no_rot:
        for i in range(1, 5):
            angle = 45 * i
            writepath = imgname + '_rot_' + angle.__str__() + '.jpg'
            print writepath
            cv2.imwrite(writepath, rotate(angle, img))
    if not arg.no_flip:
        for i in range(0, 2):
            writepath = imgname + '_flip_' + i.__str__() + '.jpg'
            print writepath
            cv2.imwrite(writepath, flip(img, i))


def rotate(angle, img):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((h/2,w/2), angle, 1)
    rot = cv2.warpAffine(img, M, (h, w))
    return rot


def flip(img, direction):
    #direction = 0 or 1.
    #0 = updown
    #1 = leftright
    return cv2.flip(img, direction)


def main(arg):
    path = arg.path
    dest = arg.dest
    if dest == None:
        dest = path

    listdir = list()
    if os.path.isdir(path):
        listdir = os.listdir(path)
    elif os.path.isfile(path):
        listdir.append(path)
    else:
        print 'DIR ERROR: ' + path
    
    for imgname in listdir:
        fullpath = os.path.join(path,imgname)
        increase_img(fullpath, arg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", 
        default=None, 
        type=str
    )
    parser.add_argument(
        "--dest", 
        default=None 
    )
    parser.add_argument(
        "--all", 
        action='store_true',
        default=False, 
    )
    parser.add_argument(
        "--no_rot", 
        action='store_true',
        default=False, 
    )
    parser.add_argument(
        "--no_flip", 
        action='store_true',
        default=False, 
    )
    arg = parser.parse_args()
    main(arg)
