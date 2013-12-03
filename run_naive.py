import naive_bayes as nb
import nltk
import random

bad_training_raw = nb.get_comment_data('bad.txt', 1)
bad_training_features = [(nb.get_features(comment), val) for (comment, val) in bad_training_raw.items()]

good_training_raw = nb.get_comment_data('good.txt', -1)
good_training_features = [(nb.get_features(comment), val) for (comment, val) in good_training_raw.items()]

combined_feature_sets = bad_training_features +  good_training_features

random.shuffle(combined_feature_sets)
size = int(len(combined_feature_sets) * 0.9)
train_set, test_set = combined_feature_sets[size:], combined_feature_sets[:size]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print classifier

print nltk.classify.accuracy(classifier, test_set)

