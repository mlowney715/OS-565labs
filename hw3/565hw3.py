# M. Phil Lowney, ID#01191051, ECE565F2016 HW#3-6
# Python 2.7, Ubuntu Linux
# Credit to Dan Noyes for his helpful code

# Make sure this program is in the same directory as ece565hw3.txt
# To run: python 565hw3.py

from multiprocessing import Queue, Process
from random import seed, randint
import argparse
import time
import sys

# Input Parser
parser = argparse.ArgumentParser(description = "Virtual Memory Simulator")
parser.add_argument("-d", "--debug", dest='DEBUG', help="Debugging Mode",
        action='store_true')
global args
args = parser.parse_args()
seed(0)

def generator(out_q):
    while True:
        # Request a virtual address
        v_address = randint(0,15)
        print("Virtual Address: " + str(v_address))
        out_q.put(v_address)
        time.sleep(1)

def translator(in_q, page_table, physical_memory):
    while True:
        # Get the next virtual address
        v_address = in_q.get()
        # Get the page number from the MSBs
        page_num = v_address >> 1
        # Get the offset as the LSB
        offset = v_address & 1
        (frame_num, pa) = page_table[page_num]

        print("Page number: " + str(page_num))
        print("Offset: " + str(offset))
        print("Valid (v/i): " + pa)

        # Check present/absent bit
        if pa == 'v':
            # Valid Page
            print("Frame number: " + str(frame_num))
            p_address = (frame_num << 1) | offset
            print("Physical Address: " + str(p_address)) 
        else:
            # Page Fault
            print("PAGE FAULT...")

            # Find the first page frame that is not mapped
            new = next(i for i, x in enumerate(physical_memory) 
                       if x == 'u')

            # Update the page table to the new frame number and
            # validate the bit
            page_table[page_num] = (new, 'v')
            # Mark the physical address as mapped
            physical_memory[new] = 'm'

            print("Mapped Page number " + str(page_num) + " to Frame number " +
                    str(new))

            # Return the physical address as the frame number and
            #  offset
            p_address = (new << 1) | offset
            print("Physical Address: " + str(p_address)) 
        if args.DEBUG:
            print(page_table)
            print(physical_memory)
        print


def main():
    print("Starting Simulation... ")

    with open("ece565hw03.txt", "r") as f:
        in_table = f.read().splitlines()

    physical_memory = []

    # In physical memory, there will be a 'u' for unmapped, and a 'm' for
    # mapped page frames
    for i in range(0,15):
        # List all physical memory addresses as unmapped
        physical_memory.append('u')

    page_table = []

    for i, item in enumerate(in_table):
        # Remove tab character from items
        item = item.translate(None, '\t')
        # Seperate page number and present/absent bit
        (entry,pa_bit) = list(item)
        entry = int(entry)
        if pa_bit == 'v':
            # Add to list of used virtual pages
            physical_memory[entry] = 'm'
        item = (entry, pa_bit)
        # Create the page table
        page_table.append(item)
    if args.DEBUG:
        print("Page Table Imported:")
        print(page_table)

    q = Queue()

    PAtrans = Process(target=translator, args=(q, page_table,
                                         physical_memory))
    VAgen = Process(target=generator, args=(q,))

    PAtrans.start()
    VAgen.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Simulation Ended...")
            break

    PAtrans.terminate()
    VAgen.terminate()
    sys.exit(0)

if __name__ == "__main__":
    main()
