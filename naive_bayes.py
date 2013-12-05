import nltk
import string
import re

def get_comment_data(file_path, val):
    '''
    Given a relative path of the comment file, return a hash where the keys are thc comments and the val will be the given val.
    '''
    text_file = open(file_path, "r")
    ret = {}
    comment = ""
    for line in text_file:
        if line.strip() == "##":
            if len(comment.strip()) != 0:
                ret[comment] = val
            comment = ""
        else:
            comment += line
    print "extracted %s comments." % len(ret)
    return ret

def alpha_num_ratio(comment):
    '''
    returns the ratio of alpha alpha numeric characters in the comment
    '''
    total = float(len(comment))
    if total == 0.0:
        return 0
    alpha_num = sum([1 for word in comment if word.isalnum()])
    return alpha_num/total

def num_bad_word(comment):
    '''
    returns the number of bad words in the comment
    '''
    comment = comment.lower()

    count = 0
    if 'asshole' in comment:
        count += 1
    if 'gay' in comment:
        count += 1
    if 'fuck' in comment:
        count += 1
    return count

def num_one_char_words(comment):
    '''
    returns the number of one character words in the comment
    '''
    count = 0
    words = comment.split(" ")

    for word in words:
        if len(word) == 1:
            count += 1

    return count

def num_two_char_rep(comment):
    '''
    returns the number of two similar characters in a row, such as: ssoonngg (would return 3)
    '''
    i = 0
    count = 0
    words = comment.split(" ")
    prevPair = False

    # loop trough the words in the comment
    for word in words:
        # loop through the word and evaluate every character
        # len - 1 because we need to evaluate the next char everytime
        while i < len(word) - 1:
            # This boolean stores whether there is a pair of the same characters (such as oo or nn)
            thisPair = False

            character = word[i]
            nextchar = word[i+1]

            # See whether the current 2 characters are the same
            if character == nextchar:
                thisPair = True

            # If the previous 2 characters where also the same we have a sequence that we should count
            if thisPair == True and prevPair == True:
                count +=1

            # The current pair is now the previous pair
            prevPair = thisPair
            # increase i with an extra 1 because we want to go to the next pair right away

            i += 2

    return count

def white_space_ratio(comment):
    '''
    Given a comment, returns the ratio of the length of the comment
    and the white space.
    '''
    white_space_count = float(comment.count(" "))
    return white_space_count/len(comment)

def is_number(s):
    '''
    checks to see if the char is a number
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False

def just_numeral(comment):
    '''
    @return true if comment is only numeral
    '''
    comment = comment.replace(".", "")
    comment = comment.replace(",", "")

    words = comment.split(" ")

    for c in words:
        if not is_number(c):
            return False
    return True

def just_punctuation(comment):
    '''
    @return true if comment is only numeral
    '''
    words = comment.split(" ")

    for c in words:

        for char in c:
            if char not in string.punctuation:
                return False
    return True

def avg_sentence_length(comment):
    '''
    Given a comment, returns the average sentence length.
    Splits sentence by line breaks and periods
    '''
    split_sent = re.split('.|\n| ',comment)
    lengths = [len(sent) for sent in split_sent]
    return sum(lengths)/len(lengths)

def get_features(comment):
    '''
    given a comment, returns the features associated with the comment.
    '''
    features = {}

    #longest length of consecutive char
    #continuoys line breaks #me
    #slang / foreign language

    features['avg_sent_length'] = avg_sentence_length(comment)
    features['line_breaks'] = comment.count("\n")
    features['just_num'] = just_numeral(comment)
    features['just_punct'] = just_punctuation(comment)
    features['white_space_ratio'] = white_space_ratio(comment)
    features['shortwords'] = num_one_char_words(comment)
    features['alpha_num'] = alpha_num_ratio(comment)
    features['*'] = comment.count("*")
    features['CAPS'] = comment.isupper()
    features['.com'] = '.com' in comment
    features['badword'] = num_bad_word(comment)
    features['len'] = len(comment)
    #features['2charchain'] = num_two_char_rep(comment)

    #naive and simple, just length to get it working.
    return features






