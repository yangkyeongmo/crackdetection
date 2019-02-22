import os
import argparse
import random
from shutil import copy


MAX_BUFFER_LENGTH = 100
MAX_TRY_LIMIT = 10000


def buffer_in(buffer, src, dest):
    buffer.append([src, dest])
    return buffer


def buffer_flush(buffer, do_move):
    processed_amount = 0
    for x in buffer:
        if check_file_existence(x[0], x[1]):
            if do_move:
                os.rename(x[0], x[1])
            else:
                copy(x[0], x[1])
            processed_amount += 1
    buffer = []
    return buffer, processed_amount


def check_file_existence(src, dest):
    if os.path.basename(src) == os.path.basename(dest):
        return True
    return False

def check_file_existence_bydir(src, dest_dir):
    if all(os.path.basename(src) != os.path.basename(f) for f in os.listdir(dest_dir)):
        return False
    return True


def moverandom(arg):
    path = arg.path
    dest = arg.dest
    amount = arg.amount
    path_buffer = []
    print('Start moving ' + path + ' to ' + dest + ' for ' + amount.__str__() + ' items')
    movedamount = 0
    while movedamount < amount:
        rand = random.random()
        filelist = os.listdir(path)
        if rand > 0.5:
            randidx = random.randrange(0, len(filelist))
            target_path = os.path.join(path, filelist[randidx])
            dest_path = os.path.join(dest, filelist[randidx])
            os.rename(target_path, dest_path)
            movedamount += 1
    buffer_flush(buffer=path_buffer, do_move=arg.move)
    return movedamount


def check_all_copied(filelist, destlist):
    all_copied = False
    for f_path in filelist:
        for f_dest in destlist:
            if os.path.basename(f_dest) != os.path.basename(f_path):
                all_copied = False
            else:
                all_copied = True
                break
    return all_copied


def check_copy_end(filelist, destlist, amount, end_at_amount):
    if len(filelist) == len(destlist):
        if check_all_copied(filelist, destlist):
            print("Everything is copied")
            return True
    if len(destlist) == amount and end_at_amount:
        print("Ending at amount " + amount.__str__())
        return True
    return False


def copyrandom(arg):
    path = arg.path
    dest = arg.dest
    amount = arg.amount
    end_at_amount = arg.end_at_amount
    print('Start coping ' + path + ' to ' + dest + ' for ' + amount.__str__() + ' items')
    copiedamount = 0
    existing_lists = os.listdir(dest)
    while copiedamount < amount:
        filelist = os.listdir(path)
        destlist = os.listdir(dest)
        # check if everything is copied
        if check_copy_end(filelist, destlist, amount, end_at_amount):
            break
        copy_path = ""
        # loop for MAX_TRY_LIMIT to find file not in path
        for i in range(0, MAX_TRY_LIMIT):
            randidx = random.randrange(0, len(filelist))
            copy_path = os.path.join(path, filelist[randidx])
            if not check_file_existence_bydir(src=copy_path, dest_dir=dest):
                existing_lists.append(copy_path)
                break
        copy(copy_path, dest)
        copiedamount += 1
    return copiedamount


def main(arg):
    path = arg.path
    if not os.path.exists(path):
        print("NO PATH ERROR: " + path)
        return
    dest = arg.dest
    if not os.path.exists(dest):
        os.mkdir(dest)
    amount = arg.amount
    processed_amount = 0
    if arg.move:
        processed_amount = moverandom(arg)
    else:
        processed_amount = copyrandom(arg)
    print('Jobs done for ' + processed_amount.__str__() + ' items')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p','--path',
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
