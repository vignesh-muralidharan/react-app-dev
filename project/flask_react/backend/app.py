from flask import Flask, request
import mysql.connector
import json
import configparser

configfile = r'./config.txt'

configParser = configparser.RawConfigParser()
configParser.read(configfile)
conecsection = 'connector config'
chost = configParser.get(conecsection, 'host')
cuser = configParser.get(conecsection, 'user')
cpasswd = configParser.get(conecsection, 'password')
cdatabase = configParser.get(conecsection, 'database')

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, Docker!'

@app.route('/widgets')
def get_widgets():
	mydb = mysql.connector.connect(host=chost, user=cuser,password=cpasswd, database=cdatabase)
	cursor = mydb.cursor()
	cursor.execute("SELECT * FROM widgets;")

	row_headers =['name', 'description']
	
	results = cursor.fetchall()
	json_data = []
	for result in results:
		json_data.append(dict(zip(row_headers,result)))
	return json.dumps(json_data)

@app.route('/initdb')
def db_init():
	mydb = mysql.connector.connect(host=chost, user=cuser,password=cpasswd)
	cursor = mydb.cursor()

	cursor.execute("CREATE DATABASE IF NOT EXISTS pytcheck;")
	mydb= mysql.connector.connect(host=chost, user=cuser,password=cpasswd, database=cdatabase)
	cursor = mydb.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS widgets(name VARCHAR (255), description VARCHAR(255));")
	mydb.commit()
	return 'init database'
@app.route('/cleardb')
def db_clear():
        db = mysql.connector.connect(host=chost, user=cuser,password=cpasswd, database = cdatabase)
        cursor = db.cursor()

        cursor.execute("DROP TABLE widgets;")
        cursor.execute("CREATE TABLE widgets(name VARCHAR (255), description VARCHAR(255));")
        db.commit()
        return 'database cleared'

@app.route('/addvalues')
def add_values():
	db = mysql.connector.connect(host=chost, user=cuser,password=cpasswd, database = cdatabase)
	cursor = db.cursor()
	#http post query
	cursor.execute("SELECT * from widgets;")
	vals = cursor.fetchall()
	value = len(vals)

	cursor.execute("INSERT INTO widgets VALUES('{}', '{}');".format("Value{}".format(value),"This is the value at table row number {}".format(value)))
	db.commit()
	return 'inserted value number {}'.format(value)

@app.route('/acceptData', methods = ['POST'])
def get_details():
	content = json.loads(request.data)
	_name = content["name"]
	_descript = content['description']
	con = mysql.connector.connect(host=chost,user=cuser,password=cpasswd,database = cdatabase)
	cursor = con.cursor()
	cursor.execute("INSERT INTO widgets VALUES('{}','{}');".format(_name,_descript))
	con.commit()
	return 'inserted'


if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 8000)

