import cv2
import os
import argparse

def main(path, intv, dest):
        filelist = list()
        if not os.path.exists(path):
                print("NO SUCH PATH ERROR: " + path)
                return
        if not os.path.isfile(path):
                if not os.path.isdir(path):
                        print("NOT FILE NOR DIR ERROR: " + path)
                        return
                else:
                        for file in os.listdir(path):
                                filepath = os.path.join(path,file)
                                if os.path.isfile(filepath):
                                        filelist.append(filepath)
        else:
                filelist.append(path)
                if not path[-4:] == '.jpg':
                        print("NOT IMAGE ERROR: " + path)
                        return

        if dest != "":
                if not os.path.exists(dest):
                        os.mkdir(dest)
                dir = dest
        else:
                dir = os.path.dirname(path)

        segpath = os.path.join(dir, "segs")
        if not os.path.exists(segpath):
                os.mkdir(segpath)

        for filepath in filelist:
                create_seg(filepath, dest, segpath, intv)

def create_seg(path, dest, segpath, intv):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        
        h, w = img.shape[:2]
        if h > w:
            w = w*800/h
            h = 800
        else:
            w = 800
            h = h*800/w
        img = cv2.resize(img, (w, h))
        x, y= 0, 0
        next_x, next_y = x+intv, y+intv
        while x < w:
                while y < h:
                        if x < 100:
                                if x < 10:
                                        str_x = '00' + x.__str__()
                                else:
                                        str_x = '0' + x.__str__()
                        else:
                                str_x = x.__str__()
                        
                        if y < 100:
                                if y < 10:
                                        str_y = '00' + y.__str__()
                                else:
                                        str_y = '0' + y.__str__()
                        else:
                                str_y = y.__str__()
                        
                        write_path = os.path.join(segpath, str_x + str_y)
                        original_write_path = write_path
                        i=0
                        while os.path.exists(write_path + '.jpg'):
                                write_path = original_write_path + '(' + i.__str__() + ')'
                                i = i +1
                        write_path = write_path + '.jpg'
                        print(write_path)
                        trimed = img[y:next_y, x:next_x]
                        cv2.imwrite(write_path, trimed)
                        y = y + intv
                        if next_y + intv > h:
                                next_y = h
                        else:
                                next_y = next_y + intv
                x = x + intv
                if next_x + intv > w:
                        next_x = w
                else:
                        next_x = next_x + intv
                y = 0
                next_y = y + intv

if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", action="store")
        parser.add_argument("--intv", action="store", type=int)
        parser.add_argument("--dest", action="store")
        arg = parser.parse_args()
        main(arg.path, arg.intv, arg.dest)
