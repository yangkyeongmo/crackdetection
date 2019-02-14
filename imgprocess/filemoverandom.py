import os
import argparse
import random
from shutil import copyfile

def main(arg):
    path = arg.path
    if not os.path.exists(path):
        print "NO PATH ERROR: " + path
        return
    dest = arg.dest
    if not os.path.exists(dest):
        os.mkdir(dest)
    amount = arg.amount
    print 'Start moving ' + path + ' to ' + dest + ' for ' + amount.__str__() + ' items'
    
    movedamount = 0
    filelist = os.listdir(path)
    while movedamount < amount:
        rand = random.random()
        if rand > 0.5:
            randidx = random.randrange(0, len(filelist))
            randfile = filelist[randidx]
            filelist.remove(randfile)
            target_path = os.path.join(path,randfile)
            target_dest = os.path.join(dest,randfile)
            if arg.copy:
                copyfile(target_path, target_dest)
            else:
                os.rename(target_path, target_dest)
            movedamount = movedamount + 1
    print 'Jobs done for ' + movedamount.__str__() + ' items'
    if arg.copy:
        print 'Copied'


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
                action = 'store',
                type=int
        )
        parser.add_argument(
            "--copy",
            action = 'store_true',
        )
        
	arg = parser.parse_args()
	main(arg)
