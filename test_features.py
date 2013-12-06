import string
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

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

def consecutive_char(comment):
    '''
    Returns the length of the longest consecutive characters chain
    '''
    words = comment.split(" ")
    chainLen = 1
    longestChain = 1

    # Loop through the words to find a long chain
    for word in words:
        for i in range(len(word) - 1):
            if(word[i] == word[i+1]):
                chainLen += 1
            else:
                if chainLen > longestChain:
                    longestChain = chainLen
                chainLen = 1
        if chainLen > longestChain:
            longestChain = chainLen

    return longestChain

def detect_language(comment):
    '''
    To detect language we could compare a comment to stopwords from each language. The language that has most
    stopwords in common with the comment is likely to be the language in which the comment is written. This is obviously
    not waterproof, however, a well written comment would work way better than a comment written in slang or with poor
    grammar. Ultimately, this would likely result in comments that are more valuable because of their structure.
    In addition, languages that are easily distinguished from English could be detected, thus being able to compare the
    language of a comment to the actual content that is annotated in Hypothes.is, since most users won't understand
    comments in a different language anyway. 
    '''

    # first we tokenize the comment
    tokens = wordpunct_tokenize(comment)
    words = [word.lower() for word in tokens]

    languages_ratios = {}

    # Then we compare the words to the most frequent stopwords per language
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        # Calculate the language score
        languages_ratios[language] = len(common_elements)

    # Get the key with the highest value
    most_rated_language = max(languages_ratios, key=languages_ratios.get)

    return most_rated_language

print detect_language("This is written in!") # English
print detect_language("Dit is een comment") # Dutch
print detect_language("Esto esta escrito en") #Spanish
print detect_language("Detta ar skrivet pa") # Swedish



