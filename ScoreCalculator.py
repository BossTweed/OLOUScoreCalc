# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:04 2016

@author: bckin_000
"""
import sys
import os
import csv
import points
import slocos

def getNames(userpath, course):
	filelist = sorted([userpath + file for file in os.listdir(userpath) if file.endswith('.xml')])
	[allnames, allslocos] = slocos.get_slocos(filelist, course)

	#print(allnames)


def calculateRankings(userpath, seasonsize, course):
	filelist = sorted([userpath + file for file in os.listdir(userpath) if file.endswith('.xml')])

	[rposlistlist, racenumlist] = points.get_positions(filelist)
	
	runners = {}
	
	with open(userpath + "classes.txt", mode='r') as csv_file:
		reader = csv.DictReader(csv_file)
		for r in reader:
			runners[r['NAME'].upper().strip()] = r['CLASS']

	classes = list(set(runners.values()))
	
	results = {}
	for c in classes:
		currentlist = []
		for r in runners:
			if runners.get(r) == c:
				currentlist.append(r)
		
		results[c] = points.get_points(points.from_list(currentlist, rposlistlist))
		results[c].pop(0)

	# Meetdirector Bonuses!
	mds = open(userpath + '/MeetDirectors.txt', 'r')
	mdsList = mds.read().split('\n')
	mds.close()


	for i, md in enumerate(mdsList):
		for r in results:
			for dct in results[r]:
				if md.upper() == dct['name']:
					try:
						dct[racenumlist[i + 1]] = sorted([v for v in dct.values()
														  if isinstance(v, int)],
														 reverse=True)[0]
					except:
						pass

	racenumlist[1:1] = ['best', 'EntriesCounted', 'SloCo']
	#print(namelistm)
	#print(racenumlist)

	[allnames, allslocos] = slocos.get_slocos(filelist, course)

	print(allnames)
	print("-------")
	print(allslocos)

	# Men's and women's dictionaries now full of everybody's names and points for
	# each race we need to get their best *SeasonSize* scores
	from operator import itemgetter
	best = []
	i = 0
	for r in results:
		for entry in results[r]:
			#print(entry)
			if len(best) <= i:
				best.append(sorted([v for v in entry.values() if isinstance(v, int)], reverse=True)[0:seasonsize])
			else:
				best[i] = sorted([v for v in entry.values() if isinstance(v, int)], reverse=True)[0:seasonsize]
			# sorts all dictionary values into a list. The text entry (person's name)
			# is first the best *SeasonSize* points values are 1 - 12 in the list
			entry['best'] = sum(best[i])
			# sum of the 11 best entries is added to each runners dictionary under the
			# entry "sumbest11"
			entry['EntriesCounted'] = len(best[i])
			try:
				entry['SloCo'] = allslocos[allnames.index(entry['name'])]
			except ValueError:
				entry['SloCo'] = 10
			#print(entry)
		i = i + 1


	# write output .csv file.
	# men's and women's dicts are just written consecutively for now
	# would like to write this direct to google drive someday!
	outfile = open(userpath + "output.csv", "w")
	w = csv.DictWriter(outfile, fieldnames=racenumlist,
					   restval=0, extrasaction='ignore', dialect='excel')
	x = csv.writer(outfile)
	i = 0
	for r in results:
		i = i + 1
		x.writerow(["Results {0}".format(r)])
		w.writeheader()
		for entry in sorted(results[r], key=itemgetter('best'), reverse=True):
			w.writerow(entry)
		
	
	outfile.close()

		
		

userpath = input('Enter path to results files: ')
if userpath[-1] != "\\":
	userpath = userpath + "\\"
if len(sys.argv) > 1:
	if sys.argv[1] == "-names":
		getNames(userpath, "ALL")
	if sys.argv[1] == "-a":
		seasonsize = int(input('Enter the number of races to count: '))
		calculateRankings(userpath, seasonsize, "Advanced")
	if sys.argv[1] == "-b":
		seasonsize = int(input('Enter the number of races to count: '))
		calculateRankings(userpath, seasonsize, "Beginner")
else:
	seasonsize = int(input('Enter the number of races to count: '))
	calculateRankings(userpath, seasonsize, "ALL")
