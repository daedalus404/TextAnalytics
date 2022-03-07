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
    
    

def createDB():
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True, help="URL of Incident PDF")
    args = parser.parse_args()
    if args.url:
        main(args.url)