###################################
# CS B551 Fall 2016, Assignment #3
#
# Your names and user ids:
# Ganesh Iyer - iyerg
# Manan Pancholi - mpanchol
# Gagandeep Singh - singhgag
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

from math import log as Log
from TrainStatistics import TrainStatistics
from copy import deepcopy

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
ts = TrainStatistics()
posTags = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    # Calculated in the same way for all the 3 algorithms
    # P(s|w)=P(s_0)*(multiplication of emission prob)*(multiplication of transition prob)
    def posterior(self, sentence, label):
        # print("{}:{}".format(len(sentence), len(label)))
        posteriorLog = ts.getPriorTagProbability(label[0])
        # print("{}-{}".format('Start', posteriorLog))
        for i in range(0, len(sentence)-1):
            posteriorLog *= ts.getTransitionProbability(label[i+1], label[i]) * ts.getEmissionProbability(sentence[i], label[i])
            # print("{}-{}".format(label[i+1]+'/'+label[i], ts.getTransitionProbability(label[i+1], label[i])))
            # print("{}-{}".format(sentence[i]+'/'+label[i], ts.getEmissionProbability(sentence[i], label[i])))
            # print("{}-{}".format('Partial', posteriorLog))
        posteriorLog *= ts.getEmissionProbability(sentence[len(sentence)-1], label[len(label)-1])
        # print("{}-{}".format('Before LOG', posteriorLog))
        if posteriorLog != 0.0:
            posteriorLog = Log(posteriorLog)
        # print("{}-{}".format('After LOG', posteriorLog))
        return posteriorLog

    # Do the training!
    #
    def train(self, data):
        for sentence in data:
            ts.addNewSentence()
            ts.extractStatistics(sentence)
        print('Training completed...!')

    # Functions for each algorithm.
    # In the simplified model, the probability of a tag given a word only depends on the prior probability of word
    # given a tag. Just like the uni-gram model.
    # P(T/W) = arg.max P(W/Ti).P(Ti)
    def simplified(self, sentence):
        print('Simplified Model')
        # print(sentence)
        posLabels = []
        marginalProabbility = []
        for word in sentence:
            temp = []
            for tag in posTags:
                temp.append(ts.getEmissionProbability(word, tag)*ts.getPriorTagProbability(tag))
            marginalProabbility.append(max(temp))
            posLabels.append(posTags[temp.index(max(temp))])
        # print(posLabels)
        # print(marginalProabbility)
        return [[posLabels], [marginalProabbility]]
    
    def hmm(self, sentence):
        # print('--------------')
        # print(sentence)
        posLabels = []
        marginalProabbility = []
        # Since we only need the previous state information, keeping the previous state values in a list will save memory
        # Size of the Viterbi Table = Number of POS Tags available = 12
        # Initialize the Viterbi table with start probabilities
        viterbiTable = []
        for tag in posTags:
            viterbiTable.append(ts.getStartProbability(tag) * ts.getEmissionProbability(sentence[0], tag))
        # print("{}-{}".format('Viterbi Table', viterbiTable))
        marginalProabbility.append(max(viterbiTable))
        posLabels.append(posTags[viterbiTable.index(max(viterbiTable))])
        # print("{}-{}".format('POS Labels', posLabels))
        for word in sentence[1:]:
            temp = []
            for tag in posTags:
                tagLikelihood = []
                for i in range(0, len(posTags)):
                    tagLikelihood.append(
                                        viterbiTable[i] *
                                        ts.getTransitionProbability(tag, posTags[i]) *
                                        ts.getEmissionProbability(word, tag)
                                        )
                temp.append(max(tagLikelihood))
            # If all the elements in temp are 0.0, then reset the viterbiTable with initial default
            # probabilities of each tag. This will avoid the propagation of 0-probabilities to future
            # steps of Viterbi Algorithm. By doing this we have observed a significant improvement in
            # the word-accuracy - From 71.6% to 94.02%
            if max(temp) != 0.0:
                viterbiTable = deepcopy(temp)
            else:
                del viterbiTable[:]
                for tag in posTags:
                    viterbiTable.append(ts.getPriorTagProbability(tag))
                # print(viterbiTable)
            marginalProabbility.append(max(viterbiTable))
            posLabels.append(posTags[viterbiTable.index(max(viterbiTable))])
            # print("{}-{}".format('POS Labels', posLabels))
            # print("{}-{}".format('Viterbi Table', viterbiTable))
        return [[posLabels], [marginalProabbility]]

    def complex(self, sentence):
        posLabels = []
        marginalProabbility = []
        # Calculate the argmax for S1
        temp = []
        for tag in posTags:
            temp.append(ts.getStartProbability(tag) * ts.getEmissionProbability(sentence[0], tag))
        marginalProabbility.append(max(temp))
        posLabels.append(posTags[temp.index(max(temp))])
        for idx,word in enumerate(sentence[1:]):
            del temp[:]
            for i in range(0, len(posTags)):
                temp.append(
                    (ts.getTrigramProbability(posTags[i], posLabels[-2], posLabels[-1]) if idx>=2 else 1.0) *
                    ts.getTransitionProbability(posTags[i], posLabels[-1]) *
                    ts.getEmissionProbability(word, posTags[i])
                    )
            marginalProabbility.append(max(temp))
            posLabels.append(posTags[temp.index(max(temp))])
            # print("{}-{}".format('POS Labels', posLabels))
            # print("{}-{}".format('Viterbi Table', viterbiTable))
        return [[posLabels], [marginalProabbility]]


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for simplified() and complex() and is the marginal probability for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM":
            return self.hmm(sentence)
        elif algo == "Complex":
            return self.complex(sentence)
        else:
            print "Unknown algo!"

