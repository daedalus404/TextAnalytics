import sqlite3
import PyPDF2
import urllib.request
import os
import re

def pullReportPdf(url: str):    #Downloads the report pdf from the given url
    fname = re.findall(r'[^/]*.pdf', url)[-1]
    
    #Create temp directory to put pdf in
    try:
        os.mkdir(os.getcwd() + '\\temp')
    except FileExistsError:
        print("Temp Directory Already Exists")
    except:
        print("Temp Directory Creation Error - not FileExistsError")
    
    #Checks if url has already been pulled and the pdf is in the temp folder
    if(os.path.exists('temp\\' + fname)):
        print("PDF already downloaded")
    else:
        #Downloads the pdf and places it in temp directory
        try:
            urllib.request.urlretrieve(url, 'temp\\' + fname)
        except:
            print("PDF download error")
    
def extractReportData(pdfFilename: str):     #converts the pdf to text and places it into a list of entry objects (list[list[string]])
    #Checks if the file exists
    if(os.path.exists('temp\\' + pdfFilename)):
        #gets pdf and size of pdf 
        pdf=open('temp\\' + pdfFilename,'rb')
        pdfReader = PyPDF2.pdf.PdfFileReader(pdf)
        numPages = pdfReader.getNumPages()
        
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
        return []
    

def createDB(): #Creates a new sqlite database or clears the existing one if one already exists
    try:
        newDb = open("normanpd.db", "x")
        newDb.close()
    except FileExistsError:
        print("Database already exists... resetting database")
    except:
        print("Database file creation error - not FileExistsError")
        
    #Connect sqlite to the database
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()
    
    #Reset Database
    cur.execute('''DROP TABLE IF EXISTS incidents''')
    
    #Create Table
    cur.execute('''CREATE TABLE incidents (
                    incident_time TEXT,
                    incident_number TEXT,
                    incident_location TEXT,
                    nature TEXT,
                    incident_ori TEXT
                    );''')
                    
    #Saves changes and closes connection to database
    con.commit()
    con.close()

    
def addEntry(entry):    #Adds a single entry to the database
    #Connects sqlite to the database
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()

    #Execute insert
    cur.execute('''INSERT INTO incidents VALUES (?,?,?,?,?)''', entry)

    #Save changes and close connection
    con.commit()
    con.close()
    
def addEntries(entries):    #Adds a list of entries to the database
    #Connects sqlite to the database
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()

    #Execute inserts
    cur.executemany('''INSERT INTO incidents VALUES (?,?,?,?,?)''', entries)

    #Save changes and close connection
    con.commit()
    con.close()
    
def status():   #Retrieves the natures and their occurence count from the database
    #Connects sqlite to the database
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()

    #Execute select
    cur.execute('''SELECT nature, COUNT (nature) as "Number of Incidents" FROM incidents GROUP BY nature''')
    natureCount = cur.fetchall()
    #Sorts returned list of tuples
    natureCount = sorted(natureCount, key=lambda x:x[1], reverse = True)
    
    #Display natures
    for nature in natureCount:
        print(nature[0] + " | " + str(nature[1]))
    
    #Save changes and close connection
    con.commit()
    con.close()

    