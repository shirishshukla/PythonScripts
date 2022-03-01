##
# Description: Input 3 numbers, A starting number and an ending number and a number to check if divisible by.
# return a list of all the number from the start to the end inclusively that are divisible by the third number.
##

import os
import argparse

def check_devide(s, e, d):
    ret=[]
    for n in range(s, e+1):
        if n % d == 0:
            ret.append(n)
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A starting number and an ending number and a number to check if divisible by")
    parser.add_argument('-s', '--starting_number', required=True, help='A starting number')
    parser.add_argument('-e', '--ending_number', required=True, help='A starting number')
    parser.add_argument('-d', '--divisible_by', required=True, help='A number to check if divisible by')

    args = parser.parse_args()
    s=args.starting_number
    e=args.ending_number
    d=args.divisible_by
    result = check_devide(int(s), int(e), int(d))
    if result:
        print('List of all the number from the start {} to the end {} inclusively that are divisible by the {}.'.format(s, e, d))
        print(result)

## END
