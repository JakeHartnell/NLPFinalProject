import nltk

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

def get_features(comment):
    '''
    given a comment, returns the features associated with the comment.
    '''
    features = {}

    #ratio of white space
    #longest length of consecutive char
    #continuoys line breaks
    #number of line breaks
    #average length of sentence [line break vs 
    #slang / foreign language
    #just numeral?
    #boolean for punctuation

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






