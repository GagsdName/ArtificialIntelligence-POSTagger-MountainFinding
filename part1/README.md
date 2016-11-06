# a3 - Part-1 POS Tagger [iyerg-mpanchol-singhgag]

-- Model Training: We created a separate class [TrainStatistics.py] for extracting statistics from training data and estimate prior, transition and emission probabilities. We try to collect the frequencies of 4 main occurrences: Individual count of each POS tag(Let's call the associated probability as Start_Probability), Bi-Gram and Tri-Gram(Used for Complex Model) sequences of tags, word to tag mapping to aid in emission probability and finally the number of times a particular POS Tag occurs at the beginning of a sentence (Let's call the associated probability as Begin_Probability). For the HMM and Complex model, we tried to use both the Start_Probability and Begin_Probability for the start probability P(S), and found extremely minor difference in the overall accuracy.

-- Posterior Probability: Calculating the Posterior Probability of each sentence [(W1, W2,.. Wn), (S1, S2,.. Sn)] is calculated as below for all the 3 models:
P(s|w)=P(s_0)*(multiplication of emission prob)*(multiplication of transition prob)
i.e.: P(S1).P(S2/S1).P(W1/S1).P(S3/S2).P(W2/S2)....P(Wn/Sn)

-- Simplified Model: In the simplified model, the probability of a tag given a word only depends on the prior probability of word given a tag; just like the uni-gram model. The POS Tag for each word in the sentence is calculated using Bayes Law as below:
P(Ti/Wi) = arg.max P(Wi/Ti).P(Ti)

-- Hidden Markov Model: To calculate the inferences from HMM model, we have implemented the Viterbi Algorithm. One important heuristic that we used to overcome the problem of 0-Probability problem is to use the prior POS Start_Proabability instead. Initially the Viterbi model used to break when we got 0 probabilities for all entries in a particular iteration because these 0 probabilities propagated further causing POS predictions to go haywire. So at any iteration when we encountered such situation, we reset the entries for that iteration with the initial Start_Proabability for each tag. This helped us achieve a significant boost in accuracy for words from 71.6% to 94.02%.

-- Complex Model: Looking at this model, we noticed that the POS at (i-2)th position also has to be factored in while calculating the POS at i'th position. So we designed the model to include Tri-Gram sequences. Also, by including the heuristic used in previous HMM model, we were able to improve the model accuracy for words from 92.6% to 94.02%.

-- Initial Results and Performance: Below are the initial results of the 3 models. The Complex model achieved highest accuracy for both the words and sentences. Simplified Model on the other hand gave worst results among the 3 models. The performance of the system is quite fast. The training is completed in under 5 seconds for the given Training data and all the 3 models are able to label sentences in the given Test data in under a minute.

==> So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct:
   0. Ground truth:      100.00%              100.00%
     1. Simplified:       92.10%               39.30%
            2. HMM:       94.02%               48.55%
        3. Complex:       94.20%               48.70%
        
-- Additional Experimentation: To make sure that our models are not suffering from the Over-Fitting problem, we ran a few experiments wherein we modified our training set by adding a chunk of top 200 lines from Test Data and at the same time altering the Test set by adding a chunk of top 200 lines from Training data. After running test experiments, the observed accuracy for each run is more or less similar to the original result. Below are the results from the experiment:

==> So far scored 2000 sentences with 31113 words.
                   Words correct:     Sentences correct:
   0. Ground truth:      100.00%              100.00%
     1. Simplified:       92.32%               38.75%
            2. HMM:       94.18%               48.00%
        3. Complex:       94.34%               48.25%
        
==> So far scored 2000 sentences with 33260 words.
                   Words correct:     Sentences correct:
   0. Ground truth:      100.00%              100.00%
     1. Simplified:       92.59%               38.05%
            2. HMM:       94.29%               46.75%
        3. Complex:       94.42%               47.00%
        
==> So far scored 2000 sentences with 34950 words.
                   Words correct:     Sentences correct:
   0. Ground truth:      100.00%              100.00%
     1. Simplified:       92.88%               36.85%
            2. HMM:       94.55%               45.80%
        3. Complex:       94.66%               46.15%
        