# M. Phil Lowney, ID#01191051, ECE565F2016 HW#3-6
# Python 2.7, Ubuntu Linux

# Make sure this program is in the same directory as ece565hw3.txt
# To run: python memory.py

from Queue import Queue
from threading import Thread
from random import seed, randint

N = 8

seed(0)

def generator(out_q):
    for i in range(1, 128):
        # Request a virtual address
        v_address = randint(0,15)
        out_q.put(v_address)

def translator(in_q, used_q, page_table, physical_memory):
    while not(in_q.empty()):
        # Get the next virtual address
        v_address = in_q.get()
        # Get the page number from the MSBs
        page_num = v_address >> 1
        # Get the offset as the LSB
        offset = v_address & 1
        (frame_num, pa) = page_table[page_num]
        # Check present/absent bit
        if pa == 'v':
            # Valid Page
            p_address = (frame_num << 1) | offset
            in_q.task_done()
        else:
            # Page Fault
            if used_q.full():
                # All physical addresses are mapped
                # Evict the first one that was assigned
                evicted = used_q.get()
                # Update the page table to the new frame number and
                # validate the bit
                page_table[page_num] = (evicted, 'v')
                # Add the newly assigned frame number to the used queue
                used_q.put(evicted)
                # Return the physical address as the frame number and
                # offset
                p_address = (evicted << 1) | offset
                in_q.task_done()
            else:
                # Find the first page frame that is not mapped

                # Code should not get to this point if all are mapped, so
                # an error will be raised if there are none that match 
                # this criteria
                new = next(i for i, x in enumerate(physical_memory) 
                           if x == 'u')
                # Update the page table to the new frame number and
                # validate the bit
                page_table[page_num] = (new, 'v')
                # Mark the physical address as mapped
                physical_memory[new] = 'm'
                # Return the physical address as the frame number and
                # offset
                p_address = (new << 1) | offset
                in_q.task_done()


with open("ece565hw03.txt", "r") as f:
    in_table = f.read().splitlines()

physical_memory = []
# In physical memory, there will be a 'u' for unmapped, and a 'm' for
# mapped page frames
for i in range(0,15):
    physical_memory.append('u')

page_table = []
used_q = Queue(maxsize = 16)
for i, item in enumerate(in_table):
    item = item.translate(None, '\t')
    (entry,pa_bit) = list(item)
    entry = int(entry)
    if pa_bit == 'v':
        # Add to list of used virtual pages
        used_q.put(entry, 1)
        physical_memory[entry] = 'm'
    item = (entry, pa_bit)
    page_table.append(item)

q = Queue(maxsize=N)
t1 = Thread(target=translator, args=(q, used_q, page_table,
                                     physical_memory))
t2 = Thread(target=generator, args=(q,))

t1.start()
t2.start()

q.join()

print(page_table)
print(physical_memory)
