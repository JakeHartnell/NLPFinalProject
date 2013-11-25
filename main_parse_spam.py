import sys
import urllib
import os

def get_spam_catalog_dict(catalog_dir):
    ''' 
    Given a directory, returns dict of  inmail.* in the directory.
    Includes RELATIVE location of the file, as well as the name.
    dict <K,V> format of <relative_path_dir+file_name, file_name>
    Will traverse sub-directories.
    example:
    {"temp/trec07/data/inmail.1109":"inmail.1109"}
    '''
    catalogs = {}
    for curdir, dirs, files in os.walk(catalog_dir):
        for check_file in files:
            if 'inmail.' in check_file: #TODO change to regex to make fancy
                catalogs[os.path.join(curdir,check_file)] = check_file
    print "Grabbed spam catalog_dict"
    return catalogs

test = get_spam_catalog_dict("../trec07p")

print len(test)

