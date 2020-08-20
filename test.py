import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "trieu",
    password = "T123",
    database = "sim_card_management")
 
id = '3'
name  = "trieu3"
q = "INSERT INTO table1 VALUES("+id+", '"+name+"');"
q2 = "SELECT * FROM table1 "


COUNTRY_ZIP_CODE = "M5P2N7"
COUNTRY_NAME = "USA"
procedure = "call add_country('"+COUNTRY_ZIP_CODE+"', '"+COUNTRY_NAME+"');"

sql = db.cursor()

#sql.execute(q)
#db.commit()
#sql.execute(q2)

#INSERT DATA TO PROCEDURE add_country(v_ZIP_CODE, v_NAME)
sql.execute(procedure)
r = sql.fetchall()



print(r)

#print(r[1][0])

