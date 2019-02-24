import os
import argparse
import random
from shutil import copy


MAX_BUFFER_LENGTH = 100
MAX_TRY_LIMIT = 10000


def buffer_in(buffer, src, dest, do_move):
    if len(buffer) >= MAX_BUFFER_LENGTH:
        buffer = buffer_flush(buffer, do_move)
    buffer.append([src, dest])
    return buffer


def buffer_flush(buffer, do_move):
    for x in buffer:
        if do_move:
            os.rename(x[0], x[1])
        else:
            copy(x[0], x[1])
    buffer = []
    return buffer


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
            dest_path = os.path.join(dest, fielist[randidx])
            if len(path_buffer) == MAX_BUFFER_LENGTH:
                path_buffer, processed_amount = buffer_flush(buffer=path_buffer,
                                                             do_move=arg.move)
                movedamount += processed_amount
            path_buffer = buffer_in(buffer=path_buffer, src=target_path, dest=dest_path)
            # os.rename(os.path.join(path,filelist[randidx]), os.path.join(dest,filelist[randidx]))
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


def get_random_path(_from, _to, _buffer):
    _from_list = os.listdir(_from)
    for i in range(0, MAX_TRY_LIMIT):
        rand_idx = random.randomrange(0, len(_from))
        _path = os.path.join(_from, _from_list[rand_idx])
        if not check_file_existence_bydir(src=_path, dest_dir=_to)\
                or _path not in _buffer:
            return _path
    return False


def copyrandom(arg):
    print('Start coping ' + arg.path + ' to ' + arg.dest + ' for ' +
          arg.amount.__str__() + ' items')
    copied_amount = 0
    while copied_amount < amount:
        filelist = os.listdir(path)
        existing_lists = os.listdir(dest)
        # check if everything is copied
        if check_copy_end(filelist, destlist, amount, end_at_amount):
            break
        # loop for MAX_TRY_LIMIT to find file not in path
        copy_path = get_random_path(filelist, dest, existing_lists)
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
