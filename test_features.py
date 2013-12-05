import string

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

def just_numeral(comment):
    '''
    @return true if comment is only numeral
    '''
    comment = comment.replace(".", "")
    comment = comment.replace(",", "")

    print comment

    words = comment.split(" ")

    for c in words:
        if not is_number(c):
            return False
    return True

def is_number(s):
    '''
    checks to see if the char is a number
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False

def isPunctuation(comment):
    '''
    @return true if comment is only numeral
    '''
    words = comment.split(" ")

    for c in words:
        print c

        for char in c:
            if char not in string.punctuation:
                return False
    return True

print just_numeral("500..000 50,,59 40")