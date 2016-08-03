#!/usr/bin/python3.4
import arff, argparse, math, copy, random
import matplotlib.pyplot as plt

# put the attribute at vector[index] at the end of the vector, shift other attribute forward
def put_to_last(vector, index):
	temp = vector[index]
	end = len(vector)-1
	while index != end:
		vector[index] = vector[index+1]
		index = index+1
	vector[end] = temp


# remove an exclusion from the list of attributes
def arrange_attributes(exclusions):
	for i in range(0, len(exclusions)):
		for j in range(0, len(attributes)):
			if attributes[j][0] == exclusions[i]:
				put_to_last(attributes, j)
				for ex in data:
					put_to_last(ex, j)


# returns string representation of a rule. If inline = False, separate antecedents by a line
def rule2String(rule, inline):
	string = ''
	string += (rule[0][0]+'='+rule[0][1])
	if not inline: string +='\n'
	for i in range(1, len(rule)):
		string += ' and '
		string += (rule[i][0]+'='+rule[i][1])
		if not inline: string +='\n'
	return string


# generates a list of candidate antecedants based on the current antecedents for a given rule and the possible attr-val pairs
def generate(current_antes):
	# get all attr-value pairs
	constraints = []
	for attr in attributes:
		for val in attr[1]:
			constraints.append([attr[0],val])

	# add to candidate_antes the antecedents that dont share an attribute w/ current_antes
	candidate_antes = []
	for con in constraints:
		add = True
		for cur in current_antes:
			if con[0] is cur[0]: add = False
		if add: candidate_antes.append(con)

	return candidate_antes


# returns true if rule matches the example, false otherwise
def match(rule, example):
	
	for ante in rule:
		index = 0
		for i in range(0, len(attributes)): 
			if attributes[i][0] is ante[0]: index = i
		if example[index] is not ante[1]:
			return False
	return True

# get the error of the provided hypothesis on the testset  
def hypothesis_error(hypothesis, testset, targetValue):
	total = len(testset)
	correct = 0
	for ex in testset:
		matches = False
		for rule in hypothesis:
			if match(rule, ex): 
				matches = True
				break
		if matches == True and ex[-1] == targetValue: correct = correct + 1
		elif matches == False and ex[-1] != targetValue: correct = correct + 1
	return 1 - (correct / total)

# Returns a duple of the number of positive and negative examples that match the rule
def match_count(rule, positives, coveredNegatives):
	pos = 0
	neg = 0
	# count the remaining positive matches...
	for ex in positives:
		if match(rule, ex): 
			pos = pos + 1

	# and the remaining covered negative matches
	for ex in coveredNegatives:
		if match(rule, ex):
			neg = neg + 1

	return [pos, neg]


# return the number of positive matches rule1 and rule2 share
def both_match_count(rule1, rule2, positives):
	count = 0
	for ex in positives:
		if match(rule1, ex) and match(rule2, ex): 
			count = count + 1
	return count


# compute the information gain when adding and antecedent
def gain(ante, rule, oldRuleCounts, positives, coveredNegatives):

	# create a duplicate rule with the added antecedent
	newRule = copy.copy(rule)
	newRule.append(ante)
	
	# get a duple containing the positive and negative matches for the new rule
	newCounts = match_count(newRule, positives, coveredNegatives)

	# total matches for new and old rules
	oldTotalMatches = oldRuleCounts[0]+oldRuleCounts[1]
	newTotalMatches = newCounts[0]+newCounts[1]

	# if either rule match 0, return 0 gain (prevents division by 0)
	if oldTotalMatches is 0 or newTotalMatches is 0: return 0
	
	oldRatio = oldRuleCounts[0]/oldTotalMatches
	newRatio = newCounts[0]/newTotalMatches

	# get the number of positive matches the new and old rule share
	dualcount = both_match_count(rule, newRule, positives)
	
	# return 0 gain if the new rule has '0' matches
	if newRatio < .0000001: return 0
 
	if oldRatio < .0000001 and newRatio > 0: return dualcount

	# return the result of the gain formula
	return dualcount * (math.log2(newRatio) - math.log2(oldRatio))


# returns a subset of examples that match rule if keepMatch = True or a subset that does not match rule if keepMatch = False
def subset(rule, examples, keepMatch):

	newExamples = []

	for ex in examples:
		if match(rule, ex):
			if keepMatch: newExamples.append(ex)
		else: 
			if not keepMatch: newExamples.append(ex)

	return newExamples

# partitions the examples into the positive and negative groupings
def partition(examples, targetValue):
	positives = []
	negatives = []
	for ex in examples :
		if str(ex[-1]) == targetValue:
			positives.append(ex)
			continue
		else: 
			negatives.append(ex)
			continue
	return [positives, negatives]

# use k cross validation to test the algorithm
def k_validate(k, targetAttribute, targetValue, examples):
	print('Running K-Fold Validation, K =',k)

	dist = partition(examples, targetValue)
	positives = dist[0]
	negatives = dist[1]

	# randomize the examples
	random.shuffle(positives)
	random.shuffle(negatives)

	posNum = math.floor(len(positives) / k)
	negNum = math.floor(len(negatives) / k)

	posPartitions = []
	negPartitions = []

	# aggregate the positives for each 'fold'
	posSt  = 0
	posEnd = posNum
	for i in range(0, k):
		posPartitions.append(positives[posSt:posEnd])
		posSt = posEnd
		posEnd = posEnd+posNum

	# aggregate the negatives for each 'fold'
	negSt  = 0
	negEnd = negNum
	for i in range(0, k):
		negPartitions.append(negatives[negSt:negEnd])
		negSt = negEnd
		negEnd = negEnd+negNum

	meanError = 0
	for i in range(0, k):
		print('Starting',i+1,'th round of validation')

		# gather the examples not used for validating
		dataset = []
		for j in range(0, k):
			if j != i: 
				dataset += negPartitions[j]
				dataset += posPartitions[j]

		# create the hypothesis
		hypothesis = foil(targetAttribute, targetValue, dataset, True)
		ithError = hypothesis_error(hypothesis, negPartitions[i] + posPartitions[i], targetValue)
		print('ithError:', ithError)
		meanError = meanError + ithError

	print('Mean Error:', (meanError / k))
	return meanError / k


def partition_holdout(examples, targetValue):
	dist = partition(examples, targetValue)
	positives = dist[0]
	negatives = dist[1]

	# randomize the examples
	random.shuffle(positives)
	random.shuffle(negatives)

	posNum = math.floor(len(positives) / 3)
	negNum = math.floor(len(negatives) / 3)

	# get the middle third of the examples for the holdout set
	holdout = []
	holdout += positives[posNum:(posNum * 2)]
	holdout += negatives[negNum:(negNum * 2)]

	# use the rest for the training set
	newExamples = []
	newExamples += positives[0:posNum]
	newExamples += positives[(posNum*2):len(positives)]
	newExamples += negatives[0:negNum]
	newExamples += negatives[(negNum*2):len(negatives)]

	return [newExamples, holdout]

# returns 1 if rule is erroneous on example, 0 if correct
def isError(rule, ex, targetValue):
	if match(rule, ex):
		if ex[-1] != targetValue: return 1
	# else: 
	# 	if ex[-1] == targetValue: return 1
	return 0

# prune the hypothesis
def prune(hypothesis, targetValue, holdout):

	size = len(holdout)

	# evaluate each rule individually
	for rule in hypothesis:

		e = 0 # incorrect matches in the holdout
		for ex in holdout: 
			e = e + isError(rule, ex, targetValue)

		# get the error of the rule as it currently is
		baseError = e / size

		# while there is more than one antecedent to the rule
		while len(rule) > 1:

			lowestError = baseError
			anteIndex = -1

			# for every antecedent...
			for j in range(0, len(rule)):
				ante = rule[j]
				candRule = []

				# make rule that excludes that antecedent
				for i in range(0, len(rule)):
					if ante is not rule[i]: candRule.append(rule[i])

				# and get the error for that new rule
				ne = 0
				for ex in holdout: ne = ne + isError(candRule, ex, targetValue)
				candError = ne / size

				# if the new error is lower...
				if lowestError > candError: 
					anteIndex = j # remember the index of the antecedent
					lowestError = candError # and reset the lowest error

			# if there was a candidate with less error, remove that antecedant
			if anteIndex != -1:
				rule.pop(anteIndex)
			else: break

	return hypothesis


# the main body of the FOIL algorithm
def foil(targetAttribute, targetValue, examples, isVal):

	# plot data
	xs = []
	ys = []
	x = 1

	# disjunctive list of rules
	hypothesis = [] 

	# sort the examples into the corresponding positive or negative grouping
	dist = partition(examples, targetValue)
	positives = dist[0]
	negatives = dist[1]
	
	# draw the empty plot
	if not isVal: line, = axes.plot(xs, ys, 'ro')

	initPosSize = len(positives)

	# while there are still positive examples not covered...
	while positives:
		# learn a new rule...
		rule = [] # empty list of antecedents (preconditions)
		coveredNegatives = copy.copy(negatives)

		while coveredNegatives:
			# ...from possible antecedents
			candidate_antes = generate(rule)

			# find the best antecedent using the gain method as a performance measure
			newRuleCounts = match_count(rule, positives, coveredNegatives)
			best_ante = candidate_antes[0]
			best_gain = gain(best_ante, rule, newRuleCounts, positives, coveredNegatives)
			for i in range(1, len(candidate_antes)):
				cand_ante = candidate_antes[i]
				cand_gain = gain(cand_ante, rule, newRuleCounts, positives, coveredNegatives)
				if cand_gain > best_gain:
					best_ante = cand_ante
					best_gain = cand_gain

			# add the best antecedent to the rule in the making
			rule.append(best_ante)
			coveredNegatives = subset(rule, coveredNegatives, True)

		beforeLen = len(positives)
		positives = subset(rule, positives, False)
		afterLen  = len(positives)

		# if the added rule, did not cover any more positives, then the remaining examples conflict
		if beforeLen == afterLen: break

		# add the now complete rule to the hypothesis in the making
		hypothesis.append(rule)

		# if we are not performing k cross validation...
		if not isVal: 
			# print the new rule to the terminal
			print(str(x)+'. '+rule2String(rule, True))
			
			# calculate the percentag covered for display
			coverage = (initPosSize - len(positives)) / initPosSize

			ys.append(coverage)
			xs.append(x)

			# update the graph with the coverage
			plt.plot(xs,ys)
			
			x = x + 1

			line.set_ydata(ys)
			line.set_xdata(xs)

			fig.canvas.draw()
			plt.show()

	if not isVal: 
		print('DONE!')
		# block so that you can print the graph or whatever you want with it
		plt.show(block=True)

	return hypothesis

# set up the CLI argument parser
parser = argparse.ArgumentParser(description='Sequential Covering Algorithm')
parser.add_argument('-a', '--attribute', dest='target_attribute', required=True)
parser.add_argument('-v', '--value', dest='target_value', required=True)
parser.add_argument('-f', '--file', dest='filename', required=True)
parser.add_argument('-e', '--exclude', dest='exclusions', nargs='*')
parser.add_argument('-k', '--validate', dest='kval', type=int, default=0)
parser.add_argument('-p', '--prune', dest='prune', action='store_true')

args = parser.parse_args()

# get a reprensentation of the arff file
arff_file = arff.load(open(args.filename, 'r')) 

# make a shallow copy of the data and attributes for manipulation
attributes = copy.copy(arff_file['attributes'])
data = copy.copy(arff_file['data'])

# set up the performance plot
if args.kval == 0:
	plt.ion()
	fig = plt.figure()
	axes = fig.add_subplot(111)
	axes.set_title('Sequential Covering of Data Set: ' + args.filename + ' (' + args.target_value + ')')
	axes.set_xlabel('Nth Added Rule')
	axes.set_ylabel('Percent Coverage of Positives')
	axes.axis(ymin = 0, ymax = 1)

# seed the rng (applicable only for k-cross validation)
random.seed(42)

print('Start Preprocessing...')

# tally all of the attributes to disregard
totalExclusions = 0

# remove any desired exclusions
if args.exclusions: 
	totalExclusions = len(args.exclusions)
	arrange_attributes(args.exclusions)

# remove the target attribute from the list of attribute
arrange_attributes([args.target_attribute])
totalExclusions = totalExclusions + 1

for i in range(0, totalExclusions): attributes.pop()

# if pruning is desired, partition a holdout set
holdout = []
if args.prune == True:
	sets = partition_holdout(data, args.target_value)
	data = sets[0]
	holdout = sets[1]

print('...Finished Preprocessing')

if args.kval > 0: k_validate(args.kval, args.target_attribute, args.target_value, data)
else: 
	hypothesis = foil(args.target_attribute, args.target_value, data, False)
	if args.prune == True: 
		print('Pruning...')
		hypothesis = prune(hypothesis, args.target_value, holdout)
		print('Pruned Hypothesis:')
		x = 1
		for rule in hypothesis:
			print(str(x)+'. '+rule2String(rule, True))
			x = x + 1

