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

def get_features(comment):
    '''
    given a comment, returns the features associated with the comment.
    '''
    features = {}

    #number of 2 char repetition
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
    #naive and simple, just length to get it working.
    return features






