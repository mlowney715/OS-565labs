#!/usr/bin/python

# M. Phil Lowney ID:01191051, ECE565F2014 HW#2-6
# Python 2.7 - Linux
# To run - type command "python simulator.py"


def P1 0
def P2 1
def P3 2
def P4 3
def READY 0
def RUNNING 1
def BLOCKED 2


class CPU:
    def __init__(self, PC, reg, time_remain, time_used):
        self.PC = PC
        self.reg = reg
        self.cycle_time_remain = time_remain
        self.cycle_time_used = time_used

class PCB:
    def __init__(self, state, PID, pPID, PC, reg, priority, time_remain,
            time_used):
        self.state = state
        self.PID = PID
        self.pPID = pPID
        self.PC = PC
        self.reg = reg
        self.priority = priority
        self.ST = time_remain
        self.TCPU = time_used

class ProcessManager:
    def __init__(self):
        self.time = 0
        self.cpu = CPU(0,(0,0,0,0),0,0)
        self.pcb_table =(PCB(READY,0,0,0,(0,0,0,0),0,0,0), 
                         PCB(READY,0,0,0,(0,0,0,0),0,0,0),
                         PCB(READY,0,0,0,(0,0,0,0),0,0,0),
                         PCB(READY,0,0,0,(0,0,0,0),0,0,0))
        self.ready_state = Queue()
        self.running_state = P1
        self.blocked_state = Queue()

    def Scheduler(self):
        return self.ready_state.get()

    def Dispatcher(self):
        self.pcb_table[self.running_state].state = READY
        self.pcb_table[self.running_state].reg = self.cpu.reg
        self.pcb_table[self.running_state].time_remain = self.cpu.time_remain
        self.pcb_table[self.running_state].time_used = READY

with open("ece565hw02.txt", "r") as f:
    counter = 1
    for line in f:
        line.replace(' ','')
        (feild,val) = line.split(':')
        
# Ran out of time to finish and implement
