'''Event management system for a college fest.
   The tables keep records of the students 
   working as volunteers to prepare for events
   of different departments or schools, 
   represented through different clubs, so that 
   nightly permissions can be adequately granted.'''

# Import to use SQL within Python
import sqlite3

# Create a connection to the desired data base
conn = sqlite3.connect('Project.db')
c = conn.cursor()

# Create the required tables
c.execute('CREATE TABLE IF NOT EXISTS '
 'Volunteer(Student_ID TEXT PRIMARY KEY, First_Name TEXT, Last_Name TEXT, Branch TEXT, School TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS '
 'Club(Club_Name TEXT PRIMARY KEY, Start_Year NUMBER, Related_School TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS '
 'Club_Members(Student_ID TEXT, First_Name TEXT, Last_Name TEXT, Club_Name TEXT, '
 'FOREIGN KEY(Student_ID) REFERENCES Volunteer(Student_ID) ON DELETE CASCADE, '
 'FOREIGN KEY(Club_Name) REFERENCES Club(Club_Name) ON DELETE CASCADE)')
c.execute('CREATE TABLE IF NOT EXISTS '
 'Event(Event_ID TEXT PRIMARY KEY, Event_Name TEXT, Event_Date TEXT,'
 'Event_Venue TEXT, Organising_Club TEXT, Event_Head TEXT, Budget TEXT, '
 'FOREIGN KEY(Event_Head) REFERENCES Volunteer(Student_ID) ON DELETE CASCADE)')
c.execute('CREATE TABLE IF NOT EXISTS '
 'Night_Pass(Student_ID TEXT, For_Event TEXT, Issuing_Club TEXT, Start_Date TEXT, End_Date TEXT, '
 'FOREIGN KEY(Student_ID) REFERENCES Volunteer(Student_ID) ON DELETE CASCADE, '
 'FOREIGN KEY(For_Event) REFERENCES Event(Event_ID) ON DELETE CASCADE, '
 'FOREIGN KEY(Issuing_Club) REFERENCES Club(Club_Name) ON DELETE CASCADE)')


# Create the required functions to add, remove or update data in the tables

def volunteer_add(): 
	sid = input("Student ID: ") 
	fname = input("First Name: ") 
	lname = input("Last Name: ") b = input("Branch: ") 
	s = input("School: ") 
	try:
		c.execute("INSERT INTO Volunteer (Student_ID, First_Name, Last_Name, Branch, School) "
		          "VALUES (?, ?, ?, ?, ?)", (sid, fname, lname, b, s)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def club_add(): 
	name = input("Club name: ") 
	sy = input("Enter club's start year: ") 
	s = input("Enter name of affiliated school: ") 
	try: 
		c.execute("INSERT INTO CLUB (Club_Name, Start_Year, Related_School) "
		          "VALUES (?, ?, ?)", (name, sy, s)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def mem_add():
	sid = input("ID: ") 
	fname = input("First Name: ") 
	lname = input("Last Name: ") 
	cn = input("Club: ") 
	temp = c.execute("SELECT Student_ID, First_Name, Last_Name FROM Volunteer") 
	f = 1 for i in temp: 
		if sid == i[0]: 
			print("Found ID") 
			f = 0 i
			if fname == i[1] and lname == i[2]: 
				print("Found Name") 
			else: 
				print("Did not find name") 
				return 0 
	if f == 1: 
		print("Did not find ID") 
		return 0 
	print("Found everything, entry can be made") 
	try: 
		c.execute("INSERT INTO Club_Members (Student_ID, First_Name, Last_Name, Club_Name) "
	               "VALUES (?, ?, ?, ?)", (sid, fname, lname, cn)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def event_add(): 
	eid = input("ID: ") 
	ename = input("Event Name: ") 
	d = input("Event Date: ") 
	v = input("Event Venue: ") 
	cn = input("Organising Club: ") 
	h = input("Event Head: ") 
	eb = input("Event Budget: ") 
	temp = c.execute("SELECT Student_ID from Volunteer") 
	f = 1 for i in temp: 
		if h == i[0]: 
			f = 0 
	if f == 1: 
		print("Values inconsistent, entry cannot be made.") 
		return 0 
    print("Entered values consistent with existing values. Entry can be made.") 
    try: 
    	c.execute("INSERT INTO Event (Event_ID, Event_Name, Event_Date, Event_Venue, Organising_Club, "
                   "Event_Head, Budget) " "VALUES (?, ?, ?, ?, ?, ?, ?)", (eid, ename, d, v, cn, h, eb)) 
    	conn.commit()
    except: 
    	print("Invalid entry") 

def np_add(): 
	sid = input("Student ID: ") 
	e = input("Event ID: ") 
	cn = input("Issuing Authority: ") 
	d1 = input("Start Date: ") 
	d2 = input("End Date: ") 
	f1 = 1 
	f2 = 1 
	temp1 = c.execute("SELECT Student_ID from Volunteer") 
	for j in temp1: 
		if sid == j[0]: 
			print("Found Student ID") 
			f1 = 0
	temp2 = c.execute("SELECT Event_ID from Event") 
	for i in temp2: 
		if e == i[0]: 
			print("Found event") 
			f2 = 0 
	if f1 == 1: 
		print("Did not find ID") 
		return 0 
	elif f2 == 1: 
		print("Did not find event") 
		return 0 
	print("Found everything, entry can be made") 
	try: 
		c.execute("INSERT INTO Night_Pass (Student_ID, For_Event, Issuing_Club, Start_Date, End_Date) "
	               "VALUES (?, ?, ?, ?, ?)", (sid, e, cn, d1, d2)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def volunteer_remove(): 
	print("Enter the ID of the student you want to remove: ") 
	sid = input("Student ID: ") 
	temp = c.execute("SELECT Student_ID FROM Volunteer") 
	for s in temp: 
		if sid == s[0]: 
			print("Student found, deleting record") 
	try: 
		c.execute("DELETE FROM Volunteer where Student_ID like (?)", (sid,)) 
		conn.commit() 
	except: print("Invalid action") 

def club_remove(): 
	print("Enter the name of the club you want to remove: ") 
	n = input("Club name: ") 
	temp = c.execute("SELECT Club_Name FROM Club") 
	for club in temp: 
		if n == club[0]: 
			print("Name found, deleting record") 
	try: 
		c.execute("DELETE FROM Club where Club_Name like (?)", (n,)) 
		conn.commit() 
	except: print("Invalid action") 

def member_remove(): 
	print("Enter the student ID and club name to search for record: ") 
	sid = input("Student ID: ") 
	n = input("Club name: ") 
	temp = c.execute("SELECT Student_ID, Club_Name FROM Club_Members") 
	for club in temp: 
		if sid == club[0] and n == club[1]: 
			print("Record found, deleting record") 
	try: 
		c.execute("DELETE FROM Club_Members where Student_ID like (?) and Club_Name like (?)", (sid, n)) 
		conn.commit() 
	except: 
		print("Invalid action") 

def event_remove(): 
	print("Enter the ID of the event you want to remove: ") 
	eid = input("Event ID: ")
	temp = c.execute("SELECT Event_ID FROM Event") 
	for e in temp: 
		if eid == e[0]: 
			print("Event found, deleting record") 
	try: 
		c.execute("DELETE FROM Event where Event_ID like (?)", (eid,)) 
		conn.commit() 
	except: 
		print("Invalid action") 

def np_remove(): 
	print("Enter the student ID, event ID and club name to search for record: ") 
	sid = input("Student ID: ") 
	eid = input("Event ID: ") 
	n = input("Club name: ") 
	temp = c.execute("SELECT Student_ID, For_Event, Issuing_Club FROM Night_Pass") 
	for np in temp: 
		if sid == np[0] and eid == np[1] and n == np[2]: 
			print("Record found, deleting record") 
	try: 
		c.execute("DELETE FROM Night_Pass where " "Student_ID like (?) and For_Event like (?) and Issuing_Club like (?)", (sid, eid, n)) 
		conn.commit() 
	except: 
		print("Invalid action") 

def volunteer_update(): 
	sid = input("Enter the ID of the student whose record needs to be updated: ") 
	temp = c.execute("SELECT Student_ID from Volunteer") 
	f = 0 
	for i in temp: 
		if sid == i[0]: 
			print("Record found, updates can be made.") 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	print("Enter the updated details -") 
	fname = input("First Name: ") 
	lname = input("Last Name: ") 
	b = input("Branch: ") 
	s = input("School: ") 
	try: 
		c.execute("UPDATE Volunteer SET First_Name = (?), Last_Name = (?), Branch = (?), School = (?) "
		          "WHERE Student_ID = (?)", (fname, lname, b, s, sid)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def club_update(): 
	name = input("Enter the club name whose record needs to be updated: ") 
	temp = c.execute("SELECT Club_Name from Club") 
	f = 0 
	for i in temp: 
		if name == i[0]: 
			print("Record found, updates can be made.") 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	print("Enter the updated details -") 
	sy = input("Start year: ") 
	s = input("School affiliated to: ")
	try: 
		c.execute("UPDATE Club SET Start_Year = (?), Related_School = (?) WHERE Club_Name = (?)", (sy, s, name))
	    conn.commit() 
	except: 
		print("Invalid entry") 

def mem_update(): 
	sid = input("Enter the ID of the student whose record needs to be updated: ") 
	temp = c.execute("SELECT Student_ID FROM Club_Members") 
	f = 0 
	for i in temp: 
		if sid == i[0]: 
			print("Record found, updates can be made.") 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	print("Enter the updated details -") 
	fname = input("First Name: ") 
	lname = input("Last Name: ") 
	cn = input("Club: ") 
	temp1 = c.execute("SELECT Club_Name FROM Club") 
	temp2 = c.execute("SELECT First_Name, Last_Name FROM Volunteer WHERE Student_ID = (?)", (sid,)) 
	f1 = 0 
	f2 = 0 
	for j in temp1: 
		if cn == j[0]: 
			f1 = 1 
	for k in temp2: 
		if fname == k[0] and lname == k[1]: 
			f2 = 1 
	if f1 == 0 or f2 == 0: 
		print("New data inconsistent with previous data, update cannot be made.") 
		return 0 
	try: 
		c.execute("UPDATE Club_Members SET First_Name = (?), Last_Name = (?), Club_Name = (?) "
	              "WHERE Student_ID = (?)", (fname, lname, cn, sid)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def event_update(): 
	eid = input("Enter the ID of the event whose records need to be updated: ") 
	temp = c.execute("SELECT Event_ID from Event") 
	f = 0 
	for i in temp: 
		if eid == i[0]: 
			print("Record found, updates can be made.") 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	print("Enter the updated details -") 
	ename = input("Event Name: ") 
	d = input("Event Date: ") 
	v = input("Event Venue: ") 
	cn = input("Organising Club: ") 
	h = input("Event Head: ") 
	eb = input("Event Budget: ") 
	temp1 = c.execute("SELECT Student_ID FROM Volunteer") 
	temp2 = c.execute("SELECT Club_Name FROM Club") 
	f1 = 0 
	f2 = 0
	for j in temp1: 
		if h == j[0]: 
			f1 = 1 
	for k in temp2: 
		if cn == k[0]: 
			f2 = 1 
	if f1 == 0 or f2 == 0: 
		print("New data inconsistent with previous data, update cannot be made.") 
		return 0 
	try: 
		c.execute("UPDATE Event SET Event_Name = (?), Event_Date = (?), Event_Venue = (?), Organising_Club = (?), "
		          "Event_Head = (?), Budget = (?) WHERE Event_ID = (?)", (ename, d, v, cn, h, eb, eid)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def np_update(): 
	sid = input("Enter the student ID to search for record to modify: ") 
	temp = c.execute("SELECT Student_ID FROM Volunteer") 
	f = 0 
	for i in temp: 
		if sid == i[0]: 
			print("Record found, updates can be made.") 
			f = 1
	print("Enter the updated details -")
	e = input("Event ID: ")
	cn = input("Issuing Authority: ")
	d1 = input("Start Date: ")
	d2 = input("End Date: ")
	f1 = 0
	f2 = 0
	temp1 = c.execute("SELECT Event_ID from Event") 
	for j in temp1: 
		if e == j[0]: 
			f1 = 1 
	temp2 = c.execute("SELECT Club_Name from Club") 
	for k in temp2: 
		if cn == k[0]: 
			f2 = 1 
	if f1 == 0 or f2 == 0: 
		print("New data inconsistent with previous data, update cannot be made.") 
		return 0 
	try: 
		c.execute("UPDATE Night_Pass SET For_Event = (?), Issuing_Club = (?), Start_Date = (?), End_Date = (?) "
		          "WHERE Student_ID = (?)", (e, cn, d1, d2, sid)) 
		conn.commit() 
	except: 
		print("Invalid entry") 

def volunteer_view(): 
	sid = input("Enter the ID of the student to view record: ") 
	temp = c.execute("SELECT Student_ID from Volunteer") 
	f = 0 
	for i in temp: 
		if sid == i[0]: 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	res = c.execute("SELECT * FROM Volunteer WHERE Student_ID = (?)", (sid,)) 
	for row in res: 
		print("Student ID: ", row[0]) 
		print("First Name: ", row[1])
		print("Last Name: ", row[2]) 
		print("Branch: ", row[3]) 
		print("School: ", row[4]) 
		print("") 

def club_view(): 
	cn = input("Enter the name of the club to view its details: ") 
	temp = c.execute("SELECT Club_Name FROM Club") 
	f = 0 
	for i in temp: 
		if cn == i[0]: 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	res = c.execute("SELECT * FROM Club WHERE Club_Name = (?)", (cn,)) 
	for row in res: 
		print("Club Name: ", row[0]) 
		print("Start Year: ", row[1]) 
		print("School: ", row[2]) 
		print("") 

def mem_view(): 
	sid = input("Enter the Student ID to view club membership details: ") 
	temp = c.execute("SELECT Student_ID FROM Club_Members") 
	f = 0 
	for i in temp: 
		if sid == i[0]:
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	res = c.execute("SELECT * FROM Club_Members WHERE Student_ID = (?)", (sid,)) 
	for row in res: 
		print("Student ID: ", row[0]) 
		print("First Name: ", row[1]) 
		print("Last Name: ", row[2]) 
		print("Club Name: ", row[3]) 
		print("") 

def event_view(): 
	eid = input("Enter the name of the event to view its details: ") 
	temp = c.execute("SELECT Event_ID FROM Event") 
	f = 0 
	for i in temp: 
		if eid == i[0]: 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 
	res = c.execute("SELECT * FROM Event WHERE Event_ID = (?)", (eid,)) 
	for row in res: 
		print("Event ID: ", row[0]) 
		print("Event Name: ", row[1]) 
		print("Event Date: ", row[2]) 
		print("Event Venue: ", row[3]) 
		print("Organising Club: ", row[4]) 
		print("Event Head: ", row[5]) 
		print("Budget: ", row[6]) 
		print("")

def np_view(): 
	sid = input("Enter the Student ID to view night pass details: ") 
	temp = c.execute("SELECT Student_ID FROM Night_Pass")
	f = 0 
	for i in temp: 
		if sid == i[0]: 
			f = 1 
	if f == 0: 
		print("Record not found.") 
		return 0 res = c.execute("SELECT * FROM Night_Pass WHERE Student_ID = (?)", (sid,)) 
		for row in res: 
			print("Student ID: ", row[0]) 
			print("Event Number: ", row[1]) 
			print("Issuing Authority: ", row[2]) 
			print("Start Date: ", row[3]) 
			print("End Date: ", row[4]) 
			print("")
 
ch_yn = 'Y' 
while ch_yn == 'y' or ch_yn == 'Y': 
	print("Welcome to the Event Manager Database. Make your choice:") 
	print("1. View details\n"
	      "2. Add records\n"
	      "3. Remove records\n" 
	      "4. Update records\n" 
	      "5. Delete entire table\n" 
	      "6. View particular records") 
	choice1 = int(input("Enter choice number: ")) 
	print("\n") 
	if choice1 == 1: 
		print("Choose table to view:\n" 
			  "1. Volunteer\n" 
			  "2. Club\n" 
			  "3. Club_Members\n" 
			  "4. Event\n" 
			  "5. Night_Pass") 
		choice2 = int(input("Enter choice of table: ")) 
		print("") 
		if choice2 == 1: 
			result = c.execute("SELECT * FROM Volunteer") 
			for r in result: 
				print("Student ID: ", r[0]) 
				print("First Name: ", r[1]) 
				print("Last Name: ", r[2]) 
				print("Branch: ", r[3]) 
				print("School: ", r[4]) 
				print("") 
		elif choice2 == 2: 
			result = c.execute("SELECT * FROM Club") 
			for r in result: 
				print("Club Name: ", r[0]) 
				print("Start Year:", r[1]) 
				print("Affiliated School: ", r[2]) 
				print("") 
		elif choice2 == 3: 
			result = c.execute("SELECT * FROM Club_Members") 
			for r in result: 
				print("Student ID: ", r[0]) 
				print("First Name", r[1]) 
				print("Last Name: ", r[2]) 
				print("Club Name: ", r[3]) 
				print("") 
		elif choice2 == 4: 
			result = c.execute("SELECT * FROM Event") 
			for r in result: 
				print("Event ID: ", r[0]) 
				print("Event Name: ", r[1]) 
				print("Event Date: ", r[2]) 
				print("Event Venue: ", r[3])
				print("Organising Club: ", r[4]) 
				print("Event Head: ", r[5]) 
				print("Budget: ", r[6]) 
				print("") 
		elif choice2 == 5: 
			result = c.execute("SELECT * FROM Night_Pass") 
			for r in result: 
				print("Student ID: ", r[0]) 
				print("Event Number: ", r[1]) 
				print("Issuing Authority: ", r[2]) 
				print("Start Date: ", r[3]) 
				print("End Date: ", r[4]) 
				print("") 
		else: 
			print("Wrong choice made.") 
			print("") 
	elif choice1 == 2: 
		print("Choose table to add records to:\n" 
			  "1. Volunteer\n" 
			  "2. Club\n" 
			  "3. Club_Members\n" 
			  "4. Event\n" 
			  "5. Night_Pass") 
		entries = int(input("Enter the number of records you wish to enter: ")) 
		choice2 = int(input("Enter choice of table: ")) 
		if choice2 == 1: 
			for i in range(0, entries): 
				print("") 
				volunteer_add() 
				print("") 
		elif choice2 == 2: 
			for i in range(0, entries): 
				print("") 
				club_add() 
				print("") 
		elif choice2 == 3: 
			for i in range(0, entries): 
				print("") 
				ma_check = mem_add() 
				if ma_check == 0: 
					print("Problem") 
					print("") 
		elif choice2 == 4: 
			for i in range(0, entries): 
				print("") 
				e_check = event_add() 
				if e_check == 0: 
					print("Problem") 
					print("") 
		elif choice2 == 5: 
			for i in range(0, entries): 
				print("") 
				np_check = np_add() 
			if np_check == 0: 
				print("Problem") 
				print("") 
		else: print("Wrong choice made.") 
	elif choice1 == 3: 
		print("Choose table to remove records from:\n" 
			  "1. Volunteer\n" 
			  "2. Club\n" 
			  "3. Club_Members\n" 
			  "4. Event\n" 
			  "5. Night_Pass") 
		entries = int(input("Enter the number of records you wish to delete: ")) 
		choice2 = int(input("Enter choice of table: ")) 
		if choice2 == 1:
			for i in range(0, entries): 
				print("") 
				volunteer_remove() 
				print("") 
		elif choice2 == 2: 
			for i in range(0, entries): 
				print("") 
				club_remove() 
				print("") 
		elif choice2 == 3: 
			for i in range(0, entries): 
				print("") 
				member_remove() 
				print("") 
		elif choice2 == 4: 
			for i in range(0, entries): 
				print("") 
				event_remove() 
				print("") 
		elif choice2 == 5: 
			for i in range(0, entries): 
				print("") 
				np_remove() 
				print("") 
		else: 
			print("") 
			print("Wrong choice made.") 
			print("") 
	elif choice1 == 4: 
		print("Choose table whose records need to be updated:\n" 
			  "1. Volunteer\n" 
			  "2. Club\n" 
			  "3. Club_Members\n" 
			  "4. Event\n" 
			  "5. Night_Pass") 
		entries = int(input("Enter the number of records you wish to update: ")) 
		choice2 = int(input("Enter choice of table: ")) 
		if choice2 == 1: 
			for i in range(0, entries): 
				print("") 
				vu_check = volunteer_update() 
				if vu_check == 0: 
					print("Problem") 
				print("") 
		elif choice2 == 2: 
			for i in range(0, entries): 
				print("") 
				cu_check = club_update() 
				if cu_check == 0: 
					print("Problem") 
				print("") 
		elif choice2 == 3: 
			for i in range(0, entries): 
				print("") 
				mu_check = mem_update() 
				if mu_check == 0: 
					print("Problem") 
				print("") 
		elif choice2 == 4: 
			for i in range(0, entries): 
				print("") 
				eu_check = event_update() 
				if eu_check == 0: 
					print("Problem") 
				print("") 
		elif choice2 == 5: 
			for i in range(0, entries): 
				print("")
				n_check = np_update() 
				if n_check == 0: 
					print("Problem") 
				print("") 
		else: 
			print("") 
			print("Wrong choice made.") 
	elif choice1 == 5: 
		print("Choose table to delete:\n" 
			  "1. Volunteer\n" 
			  "2. Club\n" 
			  "3. Club_Members\n" 
			  "4. Event\n" 
			  "5. Night_Pass") 
		choice2 = int(input("Enter choice of table: ")) 
		if choice2 == 1: 
			print("") c.execute("DELETE FROM Volunteer") 
			conn.commit() 
			print("Table Deleted.") 
			print("") 
		elif choice2 == 2: 
			print("") 
			c.execute("DELETE FROM Club") 
			conn.commit() 
			print("Table Deleted.") 
			print("") 
		elif choice2 == 3: 
			print("") 
			c.execute("DELETE FROM Club_Members") 
			conn.commit() 
			print("Table Deleted.") 
			print("") 
		elif choice2 == 4: 
			print("") 
			c.execute("DELETE FROM Event") 
			print("Table Deleted.") 
			conn.commit() 
			print("") 
		elif choice2 == 5: 
			print("") 
			c.execute("DELETE FROM Night_Pass") 
			conn.commit() 
			print("Table Deleted.") 
			print("") 
		else: 
			print("\nWrong choice made.\n") 
	elif choice1 == 6: 
		print("Choose table to view:\n" 
			  "1. Volunteer\n" 
			  "2. Club\n" 
			  "3. Club_Members\n" 
			  "4. Event\n" 
			  "5. Night_Pass") 
		choice2 = int(input("Enter choice of table: ")) 
		print("") 
		if choice2 == 1: 
			print("") 
			vv = volunteer_view() 
			if vv == 0: 
				print("Problem") 
			print("") 
		elif choice2 == 2: 
			print("") 
			cv = club_view() 
			if cv == 0: 
				print("Problem") 
				print("")
		elif choice2 == 3: 
			print("") 
			mv = mem_view() 
			if mv == 0: 
				print("Problem") 
				print("") 
		elif choice2 == 4: 
			print("") 
			ev = event_view() 
			if ev == 0: 
				print("Problem") 
			print("") 
		elif choice2 == 5: 
			print("") 
			nv = np_view() 
			if nv == 0: 
				print("Problem") 
			print("") 
		else: 
			print("\n\nWrong choice made.\n\n") 
ch_yn = input("Do you want to continue?(y/n) ") 
print("\n\n\n") 
# input("\n\n\nPress any key to exit.")