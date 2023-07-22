# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:04 2016

@author: bckin_000
"""
import os
import csv
import points
import slocos

userpath = input('Enter path to results files: ')
filelist = sorted([userpath + file for file in os.listdir(userpath)
                   if file.endswith('.xml')])


				   
[allnames, allslocos] = slocos.get_slocos(filelist)

print(allnames)
print("-------")
print(allslocos)
