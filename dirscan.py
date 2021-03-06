#!/usr/bin/python3

# 	This script uses OWASP's DirBuster list - directory-list-2.3-medium.txt
#
# 	Copyright 2007 James Fisher
#
# 	This work is licensed under the Creative Commons
# 	Attribution-Share Alike 3.0 License. To view a copy of this
# 	license, visit http://creativecommons.org/licenses/by-sa/3.0/
# 	or send a letter to Creative Commons, 171 Second Street,
# 	Suite 300, San Francisco, California, 94105, USA.

import argparse
import queue
import sys
import time

import dirscanLib

parser = argparse.ArgumentParser(description='Simple web directory scanner.')
parser.add_argument("-d", "--directory", type=str,
                                         help="Path to directory word list. Default is directorylist.txt in location of script.",
                                         default="directorylist.txt")
parser.add_argument("-n", "--threadnumber", type=int, help="Number of threads. Default is 5 threads.", default=5)
parser.add_argument("-o", "--outfile", type=str,
                                       help="Output file directory path. Default is dirscan_result.txt in location of script.",
                                       default="dirscan_result.txt")
args, target = parser.parse_known_args()

# Check that a target website was included as an argument
try:
    if not target[0]:
        parser.print_help()
        exit()
    else:
        if not target[0].startswith("http"):
            print("Need to specify http or https at start of " + target + ".")
except IndexError:
    parser.print_help()
    exit()

# Open directory file and store all lines
with open(args.directory) as file:
    directories = file.readlines()

directory_len = len(directories)

# Instantiate global queue
queue = queue.Queue()


def main():
    # Start threads
    for i in range(args.threadnumber):
        t = dirscanLib.Dirscan(queue, target[0], output_file, directory_len)
        t.setDaemon(True)
        t.start()

    # Put entries from directories list in queue
    for directory in directories:
        try:
            queue.put(directory)
            queue.join()
        except (KeyboardInterrupt, SystemExit):
            print("\nCTRL + C detected, exiting...")
            sys.exit()


output_file = open(args.outfile, "w")
start = time.time()
main()
output_file.close()
print("Elapsed time: %s" % (time.time() - start))
