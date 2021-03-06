import feature_util as nb #used to be native_bayes, which is why it is nb
import nltk
import random
import collections
import nltk.metrics

#Grab the black list word data
blacklist = nb.get_blacklist_data('data/blacklist_words')

#get negative comment data as hash, assign val = 1 in hash
bad_training_raw = nb.grab_comment_data_dir_walk('data/', 'bad', 1)

#get positive comment data as hash, assign val = -1 in hash
good_training_raw = nb.grab_comment_data_dir_walk('data/', 'good', -1)

#get heldout data 
bad_heldout_raw = nb.grab_comment_data_dir_walk('heldout/', 'heldout_bad', 1)
good_heldout_raw = nb.grab_comment_data_dir_walk('heldout/', 'heldout_good', -1)

print "\nBeginning feature extraction"
#get the features for the negative comment data
bad_training_features = [(nb.get_features(comment, blacklist), val) for (comment, val) in bad_training_raw.items()]

#get the features for the positive comment data
good_training_features = [(nb.get_features(comment, blacklist), val) for (comment, val) in good_training_raw.items()]

#get the features for the heldout data
bad_heldout_features = [(nb.get_features(comment, blacklist), val) for (comment, val) in bad_heldout_raw.items()]
good_heldout_features = [(nb.get_features(comment, blacklist), val) for (comment, val) in good_heldout_raw.items()]

print "feature extraction complete\n"
#combine the features, and then shuffle/randomize
combined_feature_sets = bad_training_features + good_training_features
combined_heldout_sets = bad_heldout_features + good_heldout_features

random.shuffle(combined_feature_sets)

#split the data into train and test
size = int(len(combined_feature_sets) * 0.9)
train_set, test_set = combined_feature_sets[size:], combined_feature_sets[:size]

print "Begin traininig classifier"
#train the classifier using the training data
classifier = nltk.NaiveBayesClassifier.train(train_set)
#classifier = nltk.SvmClassifier.train(train_set)
#classifier = nltk.DecisionTreeClassifier.train(train_set)
#classifier = nltk.MaxentClassifier.train(train_set)
#classifier = nltk.weka.WekaClassifier.train(train_set)

#nltk.classify.rte_classify

#checking the accuracy of the training data.
print "Cross-validated accuracy: %s" % nltk.classify.accuracy(classifier, test_set)

print "Heldout accuracy: %s" % nltk.classify.accuracy(classifier, combined_heldout_sets)
print

def check_precision_recall_fmeasure(commentList):
    #checking the precision and recall of the given data set
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    # Prepare the lists with the actual tags (-1 or 1) and the classified tags for comparison
    for i, (feats, label) in enumerate(commentList):
        # Store actual tags
        refsets[label].add(i)
        # Classify
        observed = classifier.classify(feats)
        # Store the classfied tags
        testsets[observed].add(i)

    # Print the precision, recall, and F-measure for positive and negative
    print 'pos precision:', nltk.metrics.precision(refsets[-1], testsets[-1])
    print 'pos recall:', nltk.metrics.recall(refsets[-1], testsets[-1])
    print 'pos F-measure:', nltk.metrics.f_measure(refsets[-1], testsets[-1])
    print 'neg precision:', nltk.metrics.precision(refsets[1], testsets[1])
    print 'neg recall:', nltk.metrics.recall(refsets[1], testsets[1])
    print 'neg F-measure:', nltk.metrics.f_measure(refsets[1], testsets[1])
    print

print "Test data precision, recall and f-measure"
check_precision_recall_fmeasure(test_set)
print "Heldout data precision, recall and f-measure"
check_precision_recall_fmeasure(combined_heldout_sets)

def classify_with_NB(comment):
    #Given a string of comment
    #@return 1 if comment needs to be flagged
    #@returns -1 if comment is fine.
    comment_feature = (nb.get_features(comment, blacklist))
    return classifier.classify(comment_feature)

def update_good(good_comment):
    '''
    Given a known good comment, add the good_comment into the training db
    '''
    with open("data/good.txt", "a") as myfile:
        myfile.write("\n##\n")
        myfile.write(good_comment)

def update_bad(bad_comment):
    '''
    Given a known bad comment, add the ba_comment into the training db
    '''
    with open("data/bad.txt", "a") as myfile:
        myfile.write("\n##\n")
        myfile.write(bad_comment)
