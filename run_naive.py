import naive_bayes as nb
import nltk

bad_training_raw = nb.get_comment_data('bad.txt', -1)
bad_training_features = [(nb.get_features(comment), val) for (comment, val) in bad_training_raw.items()]

#good_training = nb.get_comment_data('good.txt', 1)

classifier = nltk.NaiveBayesClassifier.train(bad_training_features)

print classifier


