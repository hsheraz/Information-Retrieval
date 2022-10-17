import unittest
import preprocessor
import indexer

class TestIR(unittest.TestCase):
    
    ################## testing preprocessing functions ##################
    def test_someLinesPreprocess(self):
        #test case 1 #
        self.assertEqual(preprocessor.someLinesPreprocess("this is a test 123" ), "test\n")
        # test case 2 #
        self.assertEqual(preprocessor.someLinesPreprocess("hyphen-value this is to to see if it works" ), "hyphen-valu see work\n")
        # test case 3 #
        self.assertEqual(preprocessor.someLinesPreprocess("random punctuation - , ." ), "random punctuat\n")
        # test case 4 #
        self.assertEqual(preprocessor.someLinesPreprocess("THIS IS A TEST" ), "test\n")
     
    def test_runPreprocess(self):
        # test case 1 #
        preprocessor.runPreprocess('SmallDoc.txt','SmallDoc.processed')
        with open('SmallDoc.processed','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "$TITLE\nnew year's day\n$TEXT\ntoday new year's day\nfollow close mail post offic close mail deliv\n")
        # test case 2 #
        preprocessor.runPreprocess('SmallDoc2.txt','SmallDoc2.processed')
        with open('SmallDoc2.processed','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "$DOC LA010190-0001\n$TITLE\nnew year's day\n$TEXT\ntoday new year's day\nfollow close\n")
    
    ################## testing indexer functions ##################
    def test_runOfflineProcessing(self):
        # test case 1 - three files  dictionary_SmallDoc2, postings_SmallDoc2, docids_SmallDOC2 #
        indexer.runOfflineProcessing('SmallDoc2.processed','dictionary_SmallDoc2.txt','postings_SmallDoc2.txt',"docids_SmallDOC2.txt")
        with open('dictionary_SmallDoc2.txt','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "day                   1\nnew                   1\nyear's                1\n")
        with open('postings_SmallDoc2.txt','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "0    1\n0    1\n0    1\n")
        with open('docids_SmallDOC2.txt','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "LA010190-0001     0  new year's day\n")

        # test case 2 - three files  dictionary_SmallDoc, postings_SmallDoc, docids_SmallDOC #
        indexer.runOfflineProcessing('SmallDoc.processed','dictionary_SmallDoc.txt','postings_SmallDoc.txt',"docids_SmallDOC.txt")
        with open('dictionary_SmallDoc.txt','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "day                   1\nnew                   1\nyear's                1\n")
        with open('postings_SmallDoc.txt','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "")
        with open('docids_SmallDOC.txt','r') as f:
            contents_1 = f.read()
            self.assertEqual(contents_1, "")

if __name__ == "__main__":
    unittest.main()
