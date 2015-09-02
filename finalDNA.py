import fileinput
import copy


#The Overarching pipeline for preprocessing, the algorithm, and post-processing
def solveDNA():
	#get input, store length
	shorts = [line.strip() for line in fileinput.input()]

	#remove all sandwiched shorts
	newShorts = filter(lambda x: [x for i in shorts if x in i and x != i] == [], shorts)

	#store length
	length = len(newShorts)

	#generate initial pairings, in kn^2 time
	pairs = generatePairings(newShorts)

	#greedily merge in order, until all shorts are included in merge
	solution = greedySolver(pairs, length)

	#Get forrect part of result
	result = solution[2]
	print result


#The key solution engine of the algorithm,greedily merges pairs until all shorts 
#have been accounted for
def greedySolver(pairs, length):
	sortedPairs = pairs
	#sort pairs by weight
	sortedPairs.sort(cmp = lambda x,y: cmp(x[3], y[3]))
	sortedPairs.reverse()
	#begin with the highest weighted pair
	result = copy.copy(sortedPairs[0])
	#calculate the best forward and backward merges from that point, or dummy/placeholder edge if finished
	Forwards = [x for x in sortedPairs if x[0] == result[1] and x[1] not in result[4]]
	if Forwards:
		bestForward = Forwards[0]
	else:
		bestForward = [None,None,None,-1,None]
	Backs = [x for x in sortedPairs if x[1] == result[0] and x[0] not in result[4]]
	if Backs:
		bestBack = Backs[0]
	else:
		bestBack = [None,None,None,-1,None]
	#continuously choose the highest weighted forward or backward merge
	#stop only when every short has been included, or when no more
	#shorts can be found
	while len(result[4]) < length:
		print result
		#remove from sorted pairs any items sandwiched in result
		#sortedPairs = [pair for pair in sortedPairs if pair[2] not in [pair2[2] for pair2 in sortedPairs if pair2 != pair]]
		if bestForward[0] == None and bestBack[0] == None:
			#print "AAAAAAAAAAAAAAAHHHHHHH"
			break
		if bestForward[3] > bestBack[3]:
			result = mergePairs(result, bestForward)
			Forwards = [x for x in sortedPairs if x[0] == result[1] and x[1] not in result[4]]
			if Forwards:
				bestForward = Forwards[0]
			else:
				bestForward = [None,None,None,-1,None]
		else:
			result = mergePairs(bestBack, result)
			Backs = [x for x in sortedPairs if x[1] == result[0] and x[0] not in result[4]]
			if Backs:
				bestBack = Backs[0]
			else:
				bestBack = [None,None,None,-1,None]
	#result is now a greedily chosen merge containing every initial short
	#return it
	return result

#Merges two pairs, storing the first first item and the last last item, as well as a union of all contained shorts
def mergePairs(prefix, suffix):
	print "merging pairs:"
	print "pair 1 is - " + prefix[2]
	print "pair 2 is - "+ suffix[2]
	a = shortestPairing(prefix[2], suffix[2])
	if a:
		print "merged into" + a[0]
		if a[1] >= len(prefix[2]):
			return [suffix[0], suffix[1], a[0], a[1], prefix[4] | suffix[4]]
		elif a[1] >= len(suffix[2]):
			return [prefix[0], prefix[1], a[0], a[1], prefix[4] | suffix[4]]
		else:
			return [prefix[0], suffix[1], a[0], a[1], prefix[4] | suffix[4]]

#preprocessing to generate all initial pairings
def generatePairings(shorts):
	#returns  list like (index of prefix, index of suffix, overlapped string, overlap weight)
	resultsList = []
	shortLen = len(shorts)
	for i in range(shortLen):
		#resultsList.append([None, i, shorts[i], 0])
		#resultsList.append([i, None, shorts[i], 0])
		prefix = shorts[i]
		for j in range(shortLen):
			if j != i:
				suffix = shorts[j]
				a = shortestPairing(prefix, suffix)
				if a:
					print [i, j, a[0], a[1], set([i, j])]
					resultsList.append([i, j, a[0], a[1], set([i, j])])
	# print resultsList
	return resultsList

#find the best merge of two strings
def shortestPairing(string1,string2):
	#if string1 ends in a prefix of string 2, returns the most overlapping string
	#if no overlaps, returns None
	#otherwise, returns (string with best overlap, number of overlapping characters)
	result = None
	l1 = len(string1)
	l2= len(string2)
	for i in range(min([l1,l2]) + 1):
		if string1[l1 - i:] == string2[:i] and string2[:i]:
			result = [string1 + string2[i:], i]
	return result

#run code
solveDNA()