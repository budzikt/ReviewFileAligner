#TODO import wybranych modulow
import sys
import re
import os.path
import shutil
import glob
import xml.etree.ElementTree as ET
import io

#===============================================================================
# Do some initial stuff : get version, import correct versions
#===============================================================================
PythonVersion = int(sys.version[0])
if PythonVersion == 2:
    print('you have python version 2.x.x installed.\nCorrect modules will be loaded!')
    import HTMLparser
elif PythonVersion == 3:
    print('you have python version 3.x.x installed.\nCorrect modules will be loaded!')
    from html.parser import HTMLParser

#===============================================================================
# Internal class definitions. Poor buy who cares?
#===============================================================================
class MyHTMLParser(HTMLParser):
    
    def __init__(self, WriteFileHandle):
        HTMLParser.__init__(self, False)
        self.handleF = WriteFileHandle
        self.MatchList = [[],[],[]]
        self.MatchCnt = 0
    
    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.Offset = self.getpos()
            self.TagText = self.get_starttag_text()
            self.MatchList.append([self.Offset[0], self.Offset[1], self.TagText]) 
            
    def handle_data(self, data):
        return 0
    
    def GetData(self):
        return self.MatchList


    
        
#===============================================================================
# Remove old versions of review copies (if existing)
#===============================================================================
os.chdir('..')
FileCnt = 0
FileList = []
for file in glob.glob("*.htm"):
    FileCnt = FileCnt+1
    FileList.append(file)
if FileCnt > 1:
    #search for old ReviewCopies and remove them
    for filename in FileList:
        if "ReviewCopy" in filename:
            os.remove(filename)
    
#===============================================================================
# Concate name for working copy
#===============================================================================
WorkFile = glob.glob("*.htm")
WorkFileBareName = os.path.basename(WorkFile[0])
print('\nFile for review is:')
print(WorkFile[0])
fileReviewCopy = WorkFileBareName+"_ReviewCopy.htm"
#shutil.copyfile(WorkFile[0],fileReviewCopy)


#===============================================================================
# Go with parsing file!
#===============================================================================

#Open in text mode, to retrive string...
with open(WorkFile[0], 'r+') as content_file:
    content = content_file.read()
    ModifyHtmlParser = MyHTMLParser(content_file)
    ModifyHtmlParser.feed(content)
    Res = ModifyHtmlParser.GetData()   
    #Filter out all [] fields
    ResFilter = [x for x in Res if x]
    content_file.close()

#Open in byte mode to be able to .seek via file     
with open(fileReviewCopy, 'w+b') as content_file:
    with open(WorkFile[0], 'rb') as orginal_file:
           
        CurrentFileLine = 0
        CurrSerchMatchLine = 0
        
        for line in orginal_file:
            CurrentSoureLine = orginal_file.readline();
            if  CurrentFileLine == ResFilter[CurrSerchMatchLine][0]-1:
                
                PrevLocation = content_file.tell()
                LineContent = content_file.readline()
                content_file.seek(PrevLocation,1)
                strToWrite = "<TD>"+"MojTag"+str(LineContent)
                content_file.write(bytes(strToWrite, 'UTF-8'))
                if CurrSerchMatchLine < ResFilter.__len__()-1:
                    CurrSerchMatchLine+=1
                else:
                    break
            else:
                content_file.write(bytes(CurrentSoureLine))
            CurrentFileLine +=1
if CurrentFileLine != Res.__len__():
    print('Whoops')
else:
    print("its ok")

