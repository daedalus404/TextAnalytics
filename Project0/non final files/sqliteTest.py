import sqlite3

#create db
newDb = open("normanDB.db", "x")
newDb.close()

con = sqlite3.connect('normanDB.db')

cur = con.cursor()

#Create Table
cur.execute('''CREATE TABLE incidents (
                incident_time TEXT,
                incident_number TEXT,
                incident_location TEXT,
                nature TEXT,
                incident_ori TEXT
                );''')

#write a test entry                
cur.execute('''INSERT INTO incidents VALUES ('2/1/2022 0:04', '2022-00001588', 
                                                '15300 E LINDSEY ST', 'MVA With Injuries', 
                                                '14005');''')
                                                
con.commit()

con.close()


#test read
con = sqlite3.connect('normanDB.db')
cur = con.cursor()

cur.execute('''Select * FROM incidents''')
print(cur.fetchone())

