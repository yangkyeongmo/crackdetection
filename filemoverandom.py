import os
import argparse


def main(path, dest):



if __name__='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-p','--path',
		action='store'
	)
	parser.add_argument(
		'-d', '--dest',
		action='store'
	)
	arg = parser.parse_args()
	main(arg.path, arg.dest)
