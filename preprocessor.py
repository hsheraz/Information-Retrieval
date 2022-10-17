""" 
    preprocesssor - takes in a tokenized file to noramlize (convert tokens into lower cases), filter, removes stop words and stem each words. 
    The output of this file is a .processed file
 """
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
import re


ldoc = '$DOC'
ltit = '$TITLE'
ltxt = '$TEXT'

def someLinesPreprocess(txt):   
    ps = PorterStemmer()    
    
    sents = sent_tokenize(txt.replace('\n',' ').lower())
    sents = [word.replace(': ',':\n') for word in sents];
    sents = [re.sub(r'[0-9]+', '', word) for word in sents];
    sents = [re.sub(r' +',' ', word) for word in sents];
    
    ret = ''
    for sent in sents:  # Stop words removal and Stemming
        tokens = word_tokenize(sent)     
        tokens = [ps.stem(word) for word in tokens if not word in stopwords.words()
                  and not word in ',-:n\'t---.;```\'\'\'$)(][}{+=-#@!']   
            
        ret = ret + ' '.join(tokens) + '\n'    
    return ret.replace(" \'s","\'s")


def runPreprocess(fnin,fnou):
    fin = open(fnin, 'r')
    fou = open(fnou, 'w')
    
    docs = {'':-1}
    currAct = ''
    currTitle = ''
    currText = ''
        
    # the loop for preprocessing
    line = fin.readline()
    cnt = 1
    currAct = ''
    while 0 < len(line):
        if line.startswith(ldoc):
            docid = line[len(ldoc) : -1].strip()
            docs[docid] = cnt
            currAct = ldoc
            if 0 < len(currText):
                fou.write(someLinesPreprocess(currText))
            fou.write(line)
        elif line.startswith(ltit):
            currTitle = ''
            currAct = ltit
            fou.write(line)
        elif line.startswith(ltxt):
            currText = ''
            currAct = ltxt
            if 0 < len(currTitle):
                fou.write(someLinesPreprocess(currTitle))
            fou.write(line)
        else:
            if currAct is ltit:
                currTitle = currTitle + line
            elif currAct is ltxt:
                currText = currText + line

        cnt = cnt + 1
        line = fin.readline()

    # the last Text
    if 0 < len(currText):
        fou.write(someLinesPreprocess(currText))
    fou.write(line)
    
    fin.close()
    fou.close()
    
    docs.pop('')
    return docs

if __name__ == "__main__":
    # fnin = "documents.txt"
    
    fnin = "documents.tokenized"
    fnou = "documents.processed"
        
    docs = runPreprocess(fnin,fnou)



