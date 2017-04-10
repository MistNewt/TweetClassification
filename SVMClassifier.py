from sklearn import svm
from svmutil import *
from feature_vector import *

ob = filterTweets()

result = ob.getSVMFeatures()
problem = svm_problem(result['labels'], result['feature_vector'])
#'-q' option suppress console output
param = svm_parameter('-q')
param.kernel_type = LINEAR
classifier = svm_train(problem, param)
svm_save_model(classifierDumpFile, classifier)

#Test the classifier
test_tweets = raw_input('Enter test tweet: ')
test_feature_vector = getSVMFeatureVector(test_tweets, featureList)
#p_labels contains the final labeling result
p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),test_feature_vector, classifier)
