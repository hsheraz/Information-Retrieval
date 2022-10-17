""" 
    indexer - takes in a .processed file and outputs three files: dictionary.txt, postings.txt and docids.txt. It uses an inverted index to do the splitting. The files should give the following results:
        dictionary - <stem> <document-frequency>
        posting - <did> <tf>
        docids - <did> <start-line-number> <title> vs what the professor wanted <did> <title> <start-line-number>
 """

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
import re
import string


ldoc = '$DOC'
ltit = '$TITLE'
ltxt = '$TEXT'

def updateStemStats(txt,dicStems,did_tf,currDid):
    stems = txt.split()
    for word in stems: # collect stats for each stem
        if not word in dicStems:
            # dicStems dic tells where in the list of dics
            dicStems[word] = len(did_tf) 
            # start with count 1
            did_tf.append({currDid:1})
        else:
            #print(f"word = {word}, dicStems[word] = {dicStems[word]}, currDid = {currDid}")
            tfdic = did_tf[dicStems[word]]
            if not currDid in tfdic: # add new did
                tfdic[currDid] = 1
            else:  # increase count
                tfdic[currDid] = 1 + tfdic[currDid]

def runOfflineProcessing(fnin,fnDict,fnPost,fnDocid):
    
    fin = open(fnin, 'r')
    fDict = open(fnDict, 'w')
    fPost = open(fnPost, 'w')
    fDocid = open(fnDocid, 'w')
    maxCnt = 1e5
    
    currAct = ''
    currTitle = ''
    currText = ''
    currDocid = ''
    currDid = -1;
    
    # dictionary to tell where in the list of lists of did and tf
    dicStems = {'':-1}
    # list of dictionaries, one dic per stem, telling tf for each did
    did_tf = []    
    
    # For docids file
    docids = []
    titles = []
    startlines = []
        
    line = fin.readline()
    cnt = 0
    currAct = ''
    while 0 < len(line) and cnt < maxCnt:
        if line.startswith(ldoc): # starting new DOC
            # first take care of the previous Text
            if 0 < len(currText): # text of previous DOC
                updateStemStats(currText,dicStems,did_tf,currDid)
                
            # update current docid and did
            currDocid = line[len(ldoc) : -1].strip()
            docids.append(currDocid)
            startlines.append(cnt)
            
            currDid = currDid + 1
            
        elif line.startswith(ltit): # Starting new Title
            currTitle = ''
            currAct = ltit
            
        elif line.startswith(ltxt): # starting new Text
            # first take care of the previous Title
            if 0 < len(currTitle): # text of previous DOC
                titles.append(currTitle)
                updateStemStats(currTitle,dicStems,did_tf,currDid)

            # Start new Text
            currText = ''
            currAct = ltxt

        else: # just add the line to the text or the title
            if currAct is ltit:
                currTitle = currTitle + line
            elif currAct is ltxt:
                currText = currText + line

        cnt = cnt + 1
        line = fin.readline()
        
    dicStems.pop('')
    
    # print dictionary file with doc-freq saying in how many docs stem apears
    diclist = []
    for stem in dicStems:
        tfdic = did_tf[dicStems[stem]]
        """
        docFreq = 0
        for pos in tfdic:
            docFreq = docFreq + tfdic[pos]
        """
        diclist.append((stem,len(tfdic)))
    diclist.sort()
    for p in diclist:
        fDict.write(f"{p[0]:16} {p[1]:6}\n")
        
    # print out the postings file
    for p in diclist:
        stem = p[0]
        tfdic = did_tf[dicStems[stem]]
        for did in range(currDid +1):
            if did in tfdic:
                fPost.write(f"{did} {tfdic[did]:4}\n")
        
    # print out the docids file
    for j in range(len(docids)):
        fDocid.write(f"{docids[j]:10}  {startlines[j]:4}  {titles[j]}")
        
    
    fin.close()
    fDict.close()
    fPost.close()
    fDocid.close()


if __name__ == "__main__":

    fnin = 'documents.processed'
    
    fnDict = "dictionary.txt"
    fnPost = "postings.txt"
    fnDocid = "docids.txt"
        
    runOfflineProcessing(fnin,fnDict,fnPost,fnDocid)
    



