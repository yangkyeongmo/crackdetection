import os
import argparse
import random

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
    while movedamount < amount:
        rand = random.random()
        filelist = os.listdir(path)
        if rand > 0.5:
            randidx = random.randrange(0, len(filelist))
            os.rename(os.path.join(path,filelist[randidx]), os.path.join(dest,filelist[randidx]))
            movedamount = movedamount + 1
    print 'Jobs done for ' + movedamount.__str__() + ' items'


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
	arg = parser.parse_args()
	main(arg)
