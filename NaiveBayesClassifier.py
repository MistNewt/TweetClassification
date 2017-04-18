import nltk
import csv
from feature_vector import *

ob = filterTweets()
training_set = ob.getTrainingSet()

NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

testTweets = csv.reader(open('data/CSV/testTweets.csv','rb'),delimiter=',',quotechar='|')
tweets = []
correct = 0
wrong = 0
accuracy = 0.0
for row in testTweets:
        label = row[0]
        testTweet = row[1]
        result = NBClassifier.classify(ob.extract_features(ob.getFeatureVector(testTweet)))
        print 'Expected: '+label+' Result: '+result
        if(result == label):
                correct += 1
        else:
                wrong += 1

accuracy = correct*100/(correct+wrong)
print 'Accuracy : %lf'%(accuracy)

