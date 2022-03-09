ISE 5293 
Project 0
Zackery Herman
3/8/2022

THE CODE IN THE PACKAGE RUNS AS INTENDED TO THE BEST OF MY KNOWLEDGE. THERE IS ERROR CHECKING FOR EVERY PORTION THAT I BELIEVED COULD NATURALLY GO WRONG. THE CODE DOES NOT HAVE SUFFICIENT ERROR CHECKING FOR INTENTIONALLY MALICIOUS/OBTUSE USERS. IT DOES NOT MAKE SURE YOUR URL IS CORRECT, THAT YOU HAVENT INTRODUCED INTENTIONALLY FLAWED PDFS, AND ONLY HAS THE BARE MINIMUM OF SQL SECURITY PROTECTIONS. 

Note: The pytest files are empty for the most part and I could not get the package to properly work with pytest. It would import the package but not import anything that is imported through the __init__.py

How to run program: -------------------------------------------------------------------------
The main program can be used by calling "pipenv run python project0/main.py --incidents <url>"  or equivilant calls of the main.py file in your native python environment.

The url has to be taken from the Norman Police Department Website: https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports)
(example url https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-01_daily_incident_summary.pdf)

The program will compile the information and print out to the command line via the standard out a format as shown below:

Abdominal Pains/Problems|100
Cough|20
Sneeze|20
Breathing Problems|19
Noise Complaint|4

The program is able to be run multiple times in succession without reseting anything or modifying any files.

NOTE: THIS PROGRAM IS DESIGNED ONLY TO TAKE INCIDENT REPORTS, OTHER REPORTS NOT GARUNTEED TO WORK.

NOTE: THE VALIDITY OF THIS PROGRAM IS DEPENDENT ON THE CURRENT STATE OF THE NORMAN PD WEBSITE AS OF 3/8/2022



Developer Notes: ----------------------------------------------------------------------------

The program needs to:
-Download the data given an incident pdf url

-Extract the following fields:
--Date/time
--Incident #
--Locaiton
--Nature
--Incident ORI

-Create an SQLite database to store the data
-Insert data into the database
-Print each nature and the number of times it appears

I will need to have some kind of setup file ((()))
The program should be able to run by calling its main on the command line and pass in the url arg ((()))
Each run of the program should create a new db file ((()))
It is expected that I have tests made for each function in the program ((()))
The program will be turned in via a github link in a repocity named cs5293sp22-project0 ((()))

-------------------------------------
Downloading the data:

The data is coming from the norman police report webpage (https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports)
(example url https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-01_daily_incident_summary.pdf)

The documents are in pdf format and should just be able to be downloaded somewhere onto the machine. I was planning on just generating a folder in the file structure and placing in there. It might be good to keep them cached and ask if the user wants it redownloaded if the same url is given twice. I have decided that the files will be cashed in a temp folder that is created in the cwd, the user is not asked to redownload the file, it is just not downloaded again.

pullReportPdf(url):
-Expects the full url of the pdf intended to be downloaded.
-Creates a folder named temp in the current working directory and places pdfs in there
-Has error checking for temp dir making and pdf downloading

-------------------------------------
Extracting the fields:
The fields in the report are fairly easily distinguishable from eachother. 
-Date/time is "mm/dd/yyyy hh:mm" with all subfields truncated to remove leading 0's
-Incident number is "yyyy-########"
-Location is some mix of num and char, can have "/" or spaces, it can even be lat/long. It may be best to grab the first two fields and the last two fields and then whatever is left is the location.
-Nature is a string that can have "/" or numbers in it. It might be worth looking into if this field is chosen from a set of predefined options.
-Incident ORI is always seperated by a large amount of whitespace from the nature field. It can be any combination of numbers and characters, though seems like it is always one word. It also appears that there is a small number of options for this field to be.

Need to convert pdf to plain text/strings in order to extact the data. You cant just pull the text out of the pdf file. It is suggested I use the PyPDF2 library to do this. It looks pretty simple to use.

After creating a quick script to see how PyPDF2 works, its even better than I hoped. The library returns the text in pdf object stream order and each line is 5 seperate fields. So when it returns the text, it returns each pdf object on its own line. So every 5 lines of the output is one line of input, and no seperation functions are needed to get the fields. The assignment mentions that there are "some cells that have information on multiple lines", but I have not seen an example of this so far.

NOTE: The pdf objects for the title are not at the top of the report when converted to text. They will have to be removed manually. Specifically the "NORMAN POLICE DEPARTMENT" and "Daily Incident Summary (Public)".

NOTE: There are entries that are missing information, and these are not represented as blank fields in the pdf. So I need to figure out how to not screw up the rest of the parsing when that happens. Think it will work if I essentially split it by date and then everything between those two just gets put in one entry.

NOTE: After splitting by date, there are entries without all the fields filled out. These fields are always at least including the nature. As the point of the program is to analyze the nature of the incidents, we can just delete these from the entry list.

extractReportData(pdfFilename):
-expects the filename of the pdf that being extracted as a string (This pulls from the temp folder that the program creates, DO NOT ADD FILEPATH TO THE FILENAME!)
-The method checks if the filename given is in the temp folder before doing anything
-The method returns either a list[list[string]] containing all of the entries in [date, incident #, location, nature, incident ori] order or an empty list



--------------------------------------
SQL database:
According to the documentation for sqlite3, I need to connect to a db file, then execute sql commands as normal. Followed by a commit and close statement.

Made a quick test script to get familiar with sqlite3 in python. Works how expected. 

Might need to delete old normanDB.db when program starts, should look at project description to decide. Have decided to just reset the table instead of risking OS deletion error.

There is nothing special in the functions for the sql methods. They are just calling very standard sql queries and returning it to the python environment.

creatDB():
-Takes no input and returns nothing
-Checks to see if the database is already made and clears if it so

addEntry(entry):
-Takes in a single list entry of a report in [date, incident #, location, nature, incident ori] order
-Returns nothing

addEntries(entries):
-Takes in a list of report entries in [date, incident #, location, nature, incident ori] order
-returns nothing

---------------------------------------


Bugs: ----------------------------------------------------------------------------------------
None found in the files generated by the Norman Police Department or those caused by intentionally malicious input.