import json
import sys


def arrayTest(Arg1, Arg2, Arg3):
    # TODO
    return []


def main():
    arg_list = json.loads(raw_input())
    Arg1 = arg_list[0]
    Arg2 = arg_list[1]
    Arg3 = arg_list[2]
    output = arrayTest(Arg1, Arg2, Arg3)
    print(output)

if __name__ == '__main__':
    sys.exit(main())