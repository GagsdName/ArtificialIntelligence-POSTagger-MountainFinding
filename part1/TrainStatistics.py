'''
Created on 30-Oct-2016
This class is created to store the statistics obtained from training data.
'''
class TrainStatistics:
    # totalCount = 0 # Total number of POS_Tags/Words in the training data
    # individualCount = {} # Total number of occurrences for each POS Tag
    # sentenceStartCount = {} # Keeps track of the number of times a Tag occurs at the beginning of a sentence
    # bigramCount = {} # Counts the consecutive occurrences of any two POS Tags
    # wordToTagCount = {} # Counts the number of times a word can be mapped to a given POS Tag
  
    def __init__(self):
        self.totalCount = 0
        self.individualCount = {
                                    'adj' : 0,
                                    'adv' : 0,
                                    'adp' : 0,
                                    'conj' : 0,
                                    'det' : 0,
                                    'noun' : 0,
                                    'num' : 0,
                                    'pron' : 0,
                                    'prt' : 0,
                                    'verb' : 0,
                                    'x' : 0,
                                    '.' : 0
                                }
        self.sentenceStartCount = {
                                    'adj' : 0,
                                    'adv' : 0,
                                    'adp' : 0,
                                    'conj' : 0,
                                    'det' : 0,
                                    'noun' : 0,
                                    'num' : 0,
                                    'pron' : 0,
                                    'prt' : 0,
                                    'verb' : 0,
                                    'x' : 0,
                                    '.' : 0
                                }
        self.bigramCount = {}
        self.wordToTagCount = {}
# Extract the statistics from individual sentence and update the count/map variables accordingly
# sentence is a tuple of words (observed variables) and corresponding POS Tag (hidden variables)
    def extractStatistics(self, sentence):
        self.totalCount += len(sentence[1])
        self.sentenceStartCount[sentence[1][0]] += 1
        self.individualCount[sentence[1][0]] += 1
        temp = sentence[0][0]+'#'+sentence[1][0]
        self.wordToTagCount[temp] = (self.wordToTagCount[temp]+1) if temp in self.wordToTagCount else 1
        for i in range(1, len(sentence[0])):
            self.individualCount[sentence[1][i]] += 1
            temp = sentence[0][i]+'#'+sentence[1][i]
            self.wordToTagCount[temp] = (self.wordToTagCount[temp]+1) if temp in self.wordToTagCount else 1
            temp = sentence[1][i-1]+'#'+sentence[1][i]
            self.bigramCount[temp] = (self.bigramCount[temp]+1) if temp in self.bigramCount else 1
          
    def printStatistics(self):
        print("{}-{}".format('totalCount', self.totalCount))
        # print("{}-{}".format('sentenceStartCount', self.sentenceStartCount))
        print("{}-{}".format('individualCount', self.individualCount))
        # print("{}-{}".format('wordToTagCount', self.wordToTagCount))
        
# Returns the value of P(S) for a given POS Tag
    def getPriorTagProbability(self, tag):
        return self.individualCount[tag]/self.totalCount
# Returns the probability of the given tag to occur in the beginning of a sentence
# n = Total number of sentences in the training data
    def getStartProbability(self, tag, n):
        return self.sentenceStartCount[tag]/n if tag in self.sentenceStartCount else 0.5/n
# Returns the prior probability of tag1 given tag2: P(tag1/tag2) with Smoothing
    def getTagConditionalProbability(self, tag1, tag2):
        if self.individualCount[tag2]==0:
            return 0
        temp = tag2+'#'+tag1
        return self.bigramCount[temp]/self.individualCount[tag2] if temp in self.bigramCount else (0.5/self.individualCount[tag2])
# Returns the probability of a word (W) given a tag: P(W/S) without Smoothing
    def getWordConditionalProbability(self, word, tag):
        if self.individualCount[tag]==0:
            return 0
        temp = word+'#'+tag
        return self.wordToTagCount[temp]/self.individualCount[tag]