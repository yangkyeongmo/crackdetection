import os
import argparse
import random
from shutil import copy


MAX_TRY_LIMIT = 100


def check_file_existence_bydir(src, destlist):
    if any(os.path.basename(src) == os.path.basename(f)
           for f in destlist):
        return True
    return False


def get_copy_path(path, filelist, destlist):
    for i in range(MAX_TRY_LIMIT):
        copy_path = os.path.join(path,
                                 filelist[random.randrange(0, len(filelist))])
        if not check_file_existence_bydir(src=copy_path, destlist=destlist):
            break
    return copy_path


def check_all_copied(filelist, destlist):
    all_copied = False
    for f_path in filelist:
        for f_dest in destlist:
            if os.path.basename(f_dest) == os.path.basename(f_path):
                all_copied = True
                break
            all_copied = False
    return all_copied


def check_copy_end(filelist, destlist, amount, end_at_amount):
    if len(filelist) == len(destlist):
        if check_all_copied(filelist, destlist):
            print("Everything is copied")
            return True
    if len(destlist) == amount and end_at_amount:
        print("Ending at amount", str(amount))
        return True
    return False


def copyrandom(arg):
    print('Start coping', arg.path, 'to', arg.dest,
          'for', str(arg.amount), 'items')
    count = 0
    while count < arg.amount:
        filelist = os.listdir(arg.path)
        destlist = os.listdir(arg.dest)
        # check if everything is copied
        if check_copy_end(filelist, destlist, arg.amount, arg.end_at_amount):
            break
        copy(get_copy_path(arg.path, filelist, destlist), arg.dest)
        count += 1
    return count


def moverandom(arg):
    path = arg.path
    dest = arg.dest
    print('Start moving', path, 'to', dest, 'for', str(arg.amount), 'items')
    count = 0
    while count < arg.amount:
        filelist = os.listdir(path)
        rand_filename = filelist[random.randrange(0, len(filelist))]
        os.rename(os.path.join(path, rand_filename),
                  os.path.join(dest, rand_filename))
        count += 1
    return count


def _check_path_and_dest(path, dest):
    if not os.path.exists(path):
        print("NO PATH ERROR:", path)
        return
    if not os.path.exists(dest):
        os.mkdir(dest)


def main(arg):
    _check_path_and_dest(arg.path, arg.dest)
    processed_amount = 0
    if arg.move:
        processed_amount = moverandom(arg)
    else:
        processed_amount = copyrandom(arg)
    print('Jobs done for', str(processed_amount), 'items')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--path',
        action='store'
    )
    parser.add_argument(
        '-d', '--dest',
        action='store'
    )
    parser.add_argument(
        '-am', '--amount',
        action='store',
        type=int
    )
    parser.add_argument(
        '--move',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--end_at_amount',
        action='store_false',
        default=True
    )
    arg = parser.parse_args()
    main(arg)
