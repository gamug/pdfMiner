import fitz, os, sys, re, warnings
from langdetect import detect
from pdfMiner.toolBox.structures import structureEnglish, structureSpanish  # import filtering structures
from pdfMiner.toolBox.codeUpgrader import upgradeCode
import numpy as np
import pandas as pd


# This is main class to search into PDF
class explorePDF():
    def __init__(self, workPath, consolidate=True):
        self.workPath = workPath
        self.consolidate = consolidate
        self.rejected=[]

    def main(self):
        '''''
        This function let user analize all PDF in database.
            Input:
                workPath: This path refers to a PDF database path
                consolidate: It determine export type. Default: True
                    True: Put all PDF analysis in the same excel file
                    False: Create a report by PDF file explored
            Output:
                None: save report in self.workPath\reports as excel file
        '''''

        # Here we upgrade code and restart execution
        auxn = upgradeCode()
        if auxn:
            print('restarting code...')
            return True
        aux = pd.DataFrame(columns=['PDFNAME', 'PAGE', 'PARAGRAPH', 'WORDS', 'TEXT'])
        try:
            os.makedirs(os.path.join(self.workPath, r'reports'))
        except:
            proceed=input('reports will be erase, do you want proceed (y/n)')
            if len(re.findall(r'y.*', proceed, re.IGNORECASE))>0:
                try:
                    os.remove(os.path.join(self.workPath, r'reports\consolidate.csv'))
                    os.remove(os.path.join(self.workPath, r'reports\rejected.txt'))
                except:
                    pass
            else:
                print('process rejected')
                return False
        n=-1
        for fileName in os.listdir(self.workPath):
            if fileName.split('.')[len(fileName.split('.')) - 1]=='pdf':
                n=n+1
                if n==0:
                    header=True
                else:
                    header=False
                if self.consolidate == False:
                    self.readPDF(os.path.join(self.workPath, r'reports'), os.path.join(self.workPath, fileName))
                else:
                    summary = self.readPDF(os.path.join(self.workPath, r'reports'),
                                           os.path.join(self.workPath, fileName))
                    try:
                        summary.to_csv(os.path.join(self.workPath, 'reports', 'consolidate.csv'),
                                    mode='a', header=header)
                    except:
                        pass
        if len(self.rejected) > 0:
            with open(os.path.join(self.workPath, r'reports\rejected.txt'), 'w') as f:
                f.write(str(self.rejected))
                f.close()
        if self.consolidate == True:
            summary=pd.read_csv(os.path.join(self.workPath, 'reports', 'consolidate.csv'))
            summary.rename({'Unnamed: 0':'pdfcount'},axis='columns',inplace=True)
            summary.to_csv(os.path.join(self.workPath, 'reports', 'consolidate.csv'), mode='w')
        print('********************************************')
        print('database analized')
        print('********************************************')
        return False


    def readPDF(self, workPath, pdfName):
        '''''
        This function is base to open, process and export PDF database analysis
            Input:
                workPath: This path refers to a PDF database path
                pdfName: This is the PDF full path
                consolidate: It determine export type. Default: True
                    True: Put all PDF analysis in the same excel file
                    False: Create a report by PDF file explored
            Output:
                return summary as a pandas consolidate information
        '''''
        fileName = os.path.basename(pdfName)[0:len(os.path.basename(pdfName)) - 4]
        print(fileName)
        try:
            print(f'opening {pdfName}...')
            pdf_reader = fitz.open(pdfName)
            print('success')
        except:
            print('opening failed, adding to rejected...')
            self.rejected.append(f'{os.path.basename(pdfName)[0:len(os.path.basename(pdfName)) - 4]}: corrupted file')
            return 1
        summary = pd.DataFrame(columns=['PDFNAME', 'PAGE', 'PARAGRAPH', 'WORDS', 'TEXT'])
        structure = self.getStructure(pdf_reader, fileName)  # Defining filtering structure
        try:
            structure[0][0].symbol
        except:
            return 1
        for page in range(pdf_reader.pageCount):
            i = 0
            paragraphs = pdf_reader.loadPage(page).getText("text").split('\n')
            paragraphs = self.clarify(paragraphs)
            for paragraph in paragraphs:
                words = paragraph.split(' ')
                i = i + 1
                if len(words) > 5:
                    result, boolvalues = self.boolean(words, structure)
                    if result:
                        aux = pd.DataFrame.from_dict({'PDFNAME': [fileName], 'PAGE': [page + 1], 'PARAGRAPH': [i],
                                                      'WORDS': [self.countWords(boolvalues, structure)],
                                                      'TEXT': [paragraph]})
                        summary = summary.append(aux)
        summary = summary.reset_index(drop=True)
        if self.consolidate == False:
            summary.reset_index(drop=False, inplace=True)
            summary.to_csv(os.path.join(self.workPath, 'reports', fileName + '.csv'))
        pdf_reader.close()
        return summary

    def clarify(self, array):
        '''''
        As split function in PDF page doesn't have expected results we define this function to 
        to try make some sense in page's text.
            Input:
                array: page text splited by "\n" wich result in row split
            Output:
                return: ordered page's text in paragraphs.
        '''''
        paragraphs = []
        aux = True;
        count = -1;
        i = 0;
        while count < len(array) - 1:
            paragraphs.append('')
            aux = True
            while count < len(array) - 1 and aux == True:
                count = count + 1
                if len(array[count]) > 4:
                    paragraphs[i] = paragraphs[i] + array[count]
                    if array[count][len(array[count]) - 1] == '.' or array[count][len(array[count]) - 2] == '.' or array[count][len(array[count]) - 3] == '.' or array[count][len(array[count]) - 1] == ':' or array[count][len(array[count]) - 2] == ':' or array[count][len(array[count]) - 3] == ':':
                        i = i + 1
                        aux = False
        return paragraphs

    def boolean(self, words, structure):
        '''''
        this function check words and process criterion to acept a paragraph
            input:
                words: words from a paragraph
                structure: filtering structure
            output:
                tuple: 
                    result: boolean result
                    boolean: list with boolean criterion
        '''''
        boolean = [[obj.function(words) for obj in objlist] for objlist in structure]
        boolean
        aux = []
        result = True
        for boolist in boolean:
            if True in boolist:
                aux = True
            else:
                aux = False
            result = result and aux
        return result, boolean

    # this is the function encharged to load filter structure
    def getStructure(self, pdf_reader, fileName):
        '''''
        Charge filter into class explorePDF
            input
                pdf_reader: opened pdf object
                fileName: name from pdf opened
            output:
                list of resultSearched class: charge model in explorePDF class
        '''''
        aux1 = True; n = 0; m=-1;
        while aux1 and n < 10:
            aux2 = True; m=-1;
            while aux2 and m<20:
                paragraphs1 = pdf_reader.loadPage(np.random.randint(0, pdf_reader.pageCount)-1).getText("text")
                self.paragraphs1 = self.clarify(paragraphs1)
                paragraphs2 = pdf_reader.loadPage(np.random.randint(0, pdf_reader.pageCount)-1) .getText("text")
                self.paragraphs2 = self.clarify(paragraphs2)
                try:
                    if detect(paragraphs1) == detect(paragraphs2):
                        language = detect(paragraphs1)
                        aux2 = False
                except:
                    m=m+1
                    pass
            #set default language in case we have anormal behaviour
            if m==20:
                try:
                    language=detect(fileName)
                except:
                    language='en'
            if language == 'en':
                return structureEnglish
            elif language == 'es':
                return structureSpanish
            else:
                n = n + 1
        if n == 10:
            pdf_reader.close()
            print(f'language not supported in pdf file {fileName}')
            self.rejected.append(f'{fileName}: language not supported')
            return 1

    def countWords(self, boolvalues, structure):
        '''''
        This function is designed to obtain word ocurrence count in paragraph
            Input:
                array: paragraph splited as words
                numb: numbers mode in main function
                structure: filter structure
            Output:
                All finded words
        '''''
        aux = []
        b1 = -1
        for boolist in boolvalues:
            b2 = -1
            b1 = b1 + 1
            for boolean in boolist:
                b2 = b2 + 1
                if boolean == True:
                    aux.append(structure[b1][b2].symbol)
        return aux