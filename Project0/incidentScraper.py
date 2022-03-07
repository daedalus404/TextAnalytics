import argparse
import sqlite3
import PyPDF2
import urllib.request
import os
import re

def main(url):
    print("Step 1: Pass url string")
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
    
    print("Step 4: Convert pdf to strings")
    fname = re.findall(r'[^/]*.pdf', url)[-1]
    reports = extractReportData(fname)
    
    print("Step 5: Create database")
    createDB()
    
    print("Step 6: Enter incidents")
    addEntries(reports)
    
    print("Step 7: Report incidents")
    status()
    
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
    try:
        newDb = open("normanDB.db", "x")
        newDb.close()
        print("Database file created")
    except FileExistsError:
        print("Database already exists... resetting database")
    except:
        print("Database file creation error - not FileExistsError")
        
    con = sqlite3.connect('normanDB.db')
    cur = con.cursor()
    
    #Reset Database
    cur.execute('''DROP TABLE incidents''')
    
    #Create Table
    cur.execute('''CREATE TABLE incidents (
                    incident_time TEXT,
                    incident_number TEXT,
                    incident_location TEXT,
                    nature TEXT,
                    incident_ori TEXT
                    );''')
                    
    con.commit()
    con.close()
    
    print("Database Created")

    
def addEntry(entry):
    con = sqlite3.connect('normanDB.db')
    cur = con.cursor()

    cur.execute('''INSERT INTO incidents VALUES (?,?,?,?,?)''', entry)

    con.commit()
    con.close()
    
def addEntries(entries):
    con = sqlite3.connect('normanDB.db')
    cur = con.cursor()

    cur.executemany('''INSERT INTO incidents VALUES (?,?,?,?,?)''', entries)

    con.commit()
    con.close()
    
def status():
    con = sqlite3.connect('normanDB.db')
    cur = con.cursor()

    cur.execute('''SELECT nature, COUNT (nature) as "Number of Incidents" FROM incidents GROUP BY nature''')
    natureCount = cur.fetchall()
    natureCount = sorted(natureCount, key=lambda x:x[1], reverse = True)
    
    for nature in natureCount:
        print(nature[0] + " | " + str(nature[1]))
    
    con.commit()
    con.close()

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True, help="URL of Incident PDF")
    args = parser.parse_args()
    if args.url:
        main(args.url)
        
        
        
        
        
        
        
