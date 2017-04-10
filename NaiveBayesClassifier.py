import nltk
from feature_vector import *

ob = filterTweets()
training_set = ob.getTrainingSet()

NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

testTweet = raw_input('Enter test tweet: ')
print NBClassifier.classify(ob.extract_features(ob.getFeatureVector(testTweet)))
