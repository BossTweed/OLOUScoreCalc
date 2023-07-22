from statistics import median

def get_sec(s):
	'''
	Returns time in seconds for string input, s, of form HH:MM:SS.
	if s has no colons, just returns int(s)
	'''
	l = s.split(':')
	if len(l) == 1:
		return int(l[0])
	elif len(l) == 2:
		return int(int(l[0]) * 60 + int(l[1]))
	else:
		return int(int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]))


def get_slocos(filelist, course):

	# Men and women all go in one list since were handicapping absolute times
	namelist = [{}]  # Initialize dictionary list of names and race times

	# Now we are ready to go through the results files and write everyone's point values
	# to their entry in namelist
	import xml.etree.ElementTree as ET
	racenumlist = ["name"]

	# Load each file and make string for the race number
	i = 1
	for file in filelist:

		# Read file and remove namespaces if they exist (IOF XML v3)
		it = ET.iterparse(file)
		for _, el in it:
			if '}' in el.tag:
				el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
		root = it.root

		#breakpoint()


		# take only the first class result in file. (sometimes there's a
		# reverse course or something at the end)
		if course == "ALL":
			races = root.findall("./ClassResult")
			#print(races)
		else:
			for elem in root:
				#print(elem.tag)
				if elem.tag == "ClassResult":
					courseelem = elem.find('Course')
					coursename = courseelem.find('Name').text
					if coursename == course:
						#print(coursename)
						races = [elem]
						#print(races)

		for ClassResults in races:
			racenumstr = "race" + str(i)
			i = i + 1
			# builds a list of strings corresponding to the sequence of races
			racenumlist.append(racenumstr)

			for ClassResult in ClassResults:
				# Now we're in a loop iterating through the person results
				for PersonResult in ClassResult.iter("PersonResult"):
				
					# Record rpos to determine if runner MP
					# IOF XML v2 stores it in ResultPosition,
					# IOF XML v3 stores it in Position
					for ResultPosition in PersonResult.iter('ResultPosition'):
						rpos = ResultPosition.text
					
					for ResultPosition in PersonResult.iter('Position'):
						rpos = ResultPosition.text

					if (rpos is None) or (rpos == -1):
						break

					namestr = ""
					x = 0  # A variable to keep track of whether the runner's name already exists in namelist

					# Write the runners name to namestr
					for Given in PersonResult.iter("Given"):
						try:
							namestr = namestr + Given.text + " "
						except:
							break

					for Family in PersonResult.iter("Family"):
						try:
							namestr = namestr + Family.text
						except:
							break

					namestr = namestr.upper().strip()
					
					for Time in PersonResult.findall("./Result/Time"):
						timestr = Time.text
						timeval = get_sec(timestr)
						break
					
					#print(namelist)
					for entry in namelist:

						if namestr in entry.values():
							entry[racenumstr] = timeval
							x = 1
							#print(entry)
					if x == 0:
						namelist.append({"name": namestr,
										 racenumstr: timeval})
						#print(namelist)

					Time.clear()
					timeval = None
					ResultPosition.clear()
					rpos = None

	#print(racenumlist)
	racenumlist.pop(0)
	namelist.pop(0)

	for i, key in enumerate(racenumlist):
		racetimeslist = []
		for entry in namelist:
			if key in entry:
				racetimeslist.append(entry[key])
		wintime = float(min(racetimeslist))

		for entry in namelist:
			if key in entry:
				newkey = 'SloCo{0}'.format(i)
				entry[key] = float(entry[key]) / wintime

	allnames = []
	allslocos = []

	for entry in namelist:
		orderedslocos = sorted(
			[v for v in entry.values() if isinstance(v, float)])
		#print(entry)
		#print(orderedslocos)
		entry['SloCo'] = median(orderedslocos)
		allnames.append(entry['name'])
		allslocos.append(entry['SloCo'])
	return [allnames, allslocos]
