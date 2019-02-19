import os
import cv2

def main(path,dest):
    if os.path.isfile(path):
        crop_image(path,dest)
    elif os.path.isdir(path):
        for image_path in os.listdir(path):
            crop_image(path,image_path,dest)
    else:
        print "DIR ERROR: " + path

def crop_image(path,image_path,dest):
    img = cv2.imread(os.path.join(path,image_path))
    h, w = img.shape[:2]
    if h < w:
        smaller = h
    else:
        smaller = w
    cropped = img[h/2-smaller/2:h/2+smaller/2, w/2-smaller/2:w/2+smaller/2]  
    cropped = cv2.resize(cropped, (224,224))
    cv2.imwrite(os.path.join(dest, image_path) + '_224.jpg', cropped)  

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
    main(arg.image_path,arg.dest)
