import os
import cv2

def main(path,dest):
    if os.path.isfile(path):
        grey(path,dest)
    elif os.path.isdir(path):
        for image_path in os.listdir(path):
            grey(path,image_path,dest)
    else:
        print "DIR ERROR: " + path

def grey(path,image_path, dest):
    img = cv2.imread(os.path.join(path,image_path), cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(os.path.join(dest,image_path) + '_grey.jpg', img)  

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_path", 
        default=None, 
        help="path of image or directory")
    parser.add_argument(
        "--dest", 
        default=None, 
        help="path of destination")
    
    arg= parser.parse_args()
    main(arg.image_path, arg.dest)
