import argparse
import subprocess


def main(arg):
    f = open(arg.input_txt)
    lines = f.readlines()
    for line in lines:
        print(line)
        args = line.split('%%%')
        for i in range(0, len(args)):
            args[i] = args[i].rstrip()
            print args[i]
        subprocess.call(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_txt"
    )
    parser.add_argument(
        "--args",
    )
    parser.add_argument(
        "--command",
    )
    parser.add_argument(
        "--search_through",
        default=False,
        action="store_true")
    
    arg = parser.parse_args()
    main(arg)
