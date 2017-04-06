#!/usr/bin/python

import sys

oldkey = ()
count = 0
negcount = 0

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 6:
        # Something has gone wrong. Skip this line.
        continue

    year, month, day, hour, emotion, weekday = data_mapped
    thiskey = (year, month, day, hour, weekday)

    if oldkey and oldkey != thiskey:
        year, month, day, hour, weekday = oldkey
        print  year, "\t", month, "\t", day, "\t", weekday, "\t", hour, "\t", count, "\t", float(negcount)/float(count)
        count = 0
        negcount = 0

    oldkey = thiskey
    count += 1
    if emotion == 'neg':
        negcount += 1

year, month, day, hour, weekday = oldkey
print  year, "\t", month, "\t", day, "\t", weekday, "\t", hour, "\t", count, "\t", float(negcount)/float(count)

