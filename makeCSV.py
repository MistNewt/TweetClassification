import csv
import os

class makeCSV:
    def __init__(self):
        self.fileName=''

    def __init__(self,fileName,category):
        self.fileName = fileName
        self.category = category

    def openFile(self):
        self.fin = open(self.fileName,'r')
        self.fout = open(os.path.join(os.getcwd(),'data','CSV','alltweets.csv'),'a')

    def processFile(self):
        line = self.fin.readline()
        while(line!=''):
            line = line.strip()
            wline = []
            wline.append('|'+self.category+'|')
            wline.append('|'+line+'|')
            wr=csv.writer(self.fout)
            wr.writerow(wline)
            line = self.fin.readline()
    def __del__(self):
        self.fin.close()
        self.fout.close()

def main():
    fileName = raw_input('Enter file name:')
    category = raw_input('Enter category:')
    ob = makeCSV(fileName,category)
    ob.openFile()
    ob.processFile()

main()
            
            
        
        
