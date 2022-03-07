import argparse
import sqlite3
import PyPDF2
import urllib.request
import os
import re

def main(url):
    print("Step 1: pass url string")
    print(url)
    
    print("Step 2: Create temp directory")
    #Create temp directory
    try:
        os.mkdir(os.getcwd() + '\\temp')
    except FileExistsError:
        print("Temp Directory Already Exists")
    except:
        print("Temp Directory Creation Error - not FileExistsError")
    
    print("Step 3: Download PDF")
    pullReportPdf(url)
    
    print("Step 4: convert pdf to strings")
    fname = re.findall(r'[^/]*.pdf', url)[-1]
    reports = extractReportData(fname)
    
    
    print("\n\n")



def pullReportPdf(url: str):
    #Get filename from url
    fname = re.findall(r'[^/]*.pdf', url)[-1]
    
    #Checks if url has already been pulled
    if(os.path.exists('temp\\' + fname)):
        print("PDF already downloaded")
    else:
        #Downloads the pdf and places it in temp directory
        try:
            urllib.request.urlretrieve(url, 'temp\\' + fname)
        except:
            print("PDF download error")
    
def extractReportData(pdfFilename: str):
    #converts the pdf to text and places it into a list of entry objects (list[string])
    if(os.path.exists('temp\\' + pdfFilename)):
        #gets pdf and size of pdf 
        pdf=open('temp\\' + pdfFilename,'rb')
        pdfReader = PyPDF2.pdf.PdfFileReader(pdf)
        numPages = pdfReader.getNumPages()
        print("PDF Pages: ", numPages)
        
        #Pulls pdf contents and converts to string list
        pdfContents = ""
        for page in range(numPages):
            pdfContents += pdfReader.getPage(page).extractText()
        #Have to remove title from sting because of pdf extract order inconsistency
        pdfContents = re.sub(r'NORMAN POLICE DEPARTMENT\n', "", pdfContents)
        pdfContents = re.sub(r'Daily Incident Summary \(Public\)\n', "", pdfContents)
        
        #Collect each individual entry
        datePattern = r'(\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{1,2})'
        pdfContents = re.split(datePattern, pdfContents)
        #Remove date at bottom of report and the headers at the top
        pdfContents = pdfContents[1:-2]
        
        #Combine entries
        pdfContents = [date + data for date,data in zip(pdfContents[0::2], pdfContents[1::2])]
        incidents = []
        for entry in pdfContents:
            incidents += [entry.split("\n")[:-1]]
        
        #Remove entries that are not complete
        incidents = [entry for entry in incidents if len(entry) == 5]

        pdf.close()
        return incidents
        
    else:
        print("Error: File not found")
        return None
    

def createDB():
    print()
    
def addEntry(entry):
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True, help="URL of Incident PDF")
    args = parser.parse_args()
    if args.url:
        main(args.url)
        
        
        
        
        
        
        
