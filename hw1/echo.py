#!/usr/bin/python

# M. Phil Lowney ID:01191051, ECE565F2014 HW#-6
# Python 2.7 - Linux
# To run - type command "python echo.py"

fo = open("ece565hw01.txt", "r")
text = fo.read()
print(text)
fo.close
