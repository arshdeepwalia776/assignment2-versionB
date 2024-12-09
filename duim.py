#!/usr/bin/env python3

import subprocess
import sys
import argparse


'''
OPS445 Assignment 2
Program: duim.py 
Author: Arshdeep Walia
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: Improved `duim.py` file that tels us the disc usage.

Date: 8 december 2024
'''


def parse_command_args():
    """Set up argparse here. Call this function inside main."""
    parser = argparse.ArgumentParser(
        description="DU Improved -- See Disk Usage Report with bar charts",
        epilog="Copyright 2023")
#Argument which specify the length of the bar graph , and have the dfault length of 20 char
    parser.add_argument("-l", "--length", type=int, default=20,
                        help="Specify the length of the graph. Default is 20.")
# This print the sizes in a human - readable format
   parser.add_argument("-H", "--human-readable",action="store_true",
                        help="Show sizes in a readable format (e.g., 1K, 23M, 2G).")
#This tells which directory to scan having cureent directtory as the defauult one
    parser.add_argument("target", nargs="?", default=".",
                        help="The directory to scan. Defaults to current directory.")
#Return the parsed arguents
    return parser.parse_args()


def percent_to_graph(percent: int, total_chars: int) -> str:
    """Returns a string bar graph for a percentage."""
#Condition to check if the Provided percentage is between 0 and 100
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
# calculating how many characters sshould be filed  
    filled_chars = int(round(percent * total_chars / 100))
#Retur the result with = for filled cahr and * for the empty parrt 
   return "=" * filled_chars + " " * (total_chars - filled_chars)


def call_du_sub(location: str) -> list:
    """Use subprocess to call `du -d 1 + location`, return raw list."""
    try:
        result = subprocess.check_output(
            ["du", "-d", "1", location],
            text=True, #Returning output as a text
            stderr=subprocess.STDOUT  # Capture both stdout and stderr
        )
# Split the output into lines annd retur the output as a list
        return result.strip().split("\n")
    except subprocess.CalledProcessError as e:
        # Filter out permission denied errors
        if "Permission denied" in e.output:
            sys.stderr.write(f"Warning: Permission denied errors encountered.\n")
            return [] # return an empty list 
        else:
            sys.stderr.write(f"Error running du command: {e.output}\n")
            sys.exit(1) #Exit if there are errors


def create_dir_dict(raw_dat: list) -> dict:
    """Convert list from `du` into a dictionary with directory sizes."""
    dir_dict = {}
    for line in raw_dat:
        size, path = line.split(maxsplit=1) #Split size and path of the directory
        dir_dict[path] = int(size) # store the sie in the directory 
    return dir_dict


def bytes_to_human_r(kibibytes: int, decimal_places: int = 2) -> str:
    """Convert size in kibibytes to human-readable format."""
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    suf_count = 0
    result = kibibytes
    while result > 1024 and suf_count < len(suffixes) - 1:
        result /= 1024
        suf_count += 1
#Return the size in the result the required unit
    return f'{result:.{decimal_places}f} {suffixes[suf_count]}'


if __name__ == "__main__":
    args = parse_command_args()

    # Call du and get data
    du_output = call_du_sub(args.target)
#If no data is found print error message and exit
    if not du_output:
        print(f"No readable directories found in: {args.target}")
        sys.exit(0)
#Convert the data into dictionary of directories
    dir_data = create_dir_dict(du_output)

    # Calculate total size
    total_size = sum(dir_data.values())

    # Print formatted output
    print(f"Disk usage for: {args.target}")
    for path, size in dir_data.items():
#Calculate the perecent of the size  within the totalsize for directory
        percent = (size / total_size) * 100 if total_size else 0
#Create the bargraph based on percentage calculates result 
        bar = percent_to_graph(percent, args.length
#  Display the size in bytes if  human readable format is required
        size_display = bytes_to_human_r(size // 1024) if args.human_readable else f"{size}B"
        print(f"{percent:.0f}% [{bar}] {size_display} {path}")

    # Print total size at the end of report
    total_display = bytes_to_human_r(total_size // 1024) if args.human_readable else f"{total_size}B"
    print(f"Total: {total_display}")
