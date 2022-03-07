ISE 5293 
Project 0
Zackery Herman
3/8/2022

How to run program: -------------------------------------------------------------------------
((()))

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

The documents are in pdf format and should just be able to be downloaded somewhere onto the machine. I was planning on just generating a folder in the file structure and placing in there. It might be good to keep them cached and ask if the user wants it redownloaded if the same url is given twice.

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


--------------------------------------
Creating the SQL database:
According to the documentation for sqlite3, I need to connect to a db file, then execute sql commands as normal. Followed by a commit and close statement.

Made a quick test script to get familiar with sqlite3 in python. Works how expected. 

Might need to delete old normanDB.db when program starts, should look at project description to decide.

---------------------------------------


Bugs: ----------------------------------------------------------------------------------------
((()))