

def get_comment_data(file_path, val):
    '''
    Given a relative path of the comment file, return a hash where the keys are thc comments and the val will be the given val.
    '''
    text_file = open(file_path, "r")
    ret = {}
    comment = ""
    for line in text_file:
        if line.strip() == "##":
            ret[comment] = val
            comment = ""
        else:
            comment += line
    print "extracted %s comments." % len(ret)
    return ret

def get_features(comment):
    '''
    given a comment, returns the features associated with the comment.
    '''
    pass






