import argparse

from incidentScraper import *

def main(url):
    #Pulls report pdf from url given
    pullReportPdf(url)
    #Extracts filename from pdf file given
    fname = re.findall(r'[^/]*.pdf', url)[-1]
    #Extracts report data into a list[list[string]]
    reports = extractReportData(fname)
    #Creates the database for the report data
    createDB()
    #Adds all of the report entries to the database
    addEntries(reports)
    #Reports the nature count of all the reports
    status()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True, help="URL of Incident PDF")
    args = parser.parse_args()
    if args.url:
        main(args.url)
        
        
        
        
        
        
        
