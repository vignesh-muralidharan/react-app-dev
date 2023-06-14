from flask import Flask, request
import mysql.connector as conec
import json
import os
import configparser

configfile = r'./config.txt'
app = Flask(__name__)

configParser = configparser.RawConfigParser()
configParser.read(configfile)
conecsection = 'connector config'
cpasswd = configParser.get(conecsection, 'password')
cdb = configParser.get(conecsection, 'database')
chost = configParser.get(conecsection, 'host')


@app.route('/')
def hello_world():
	return 'Hello, Docker!'

@app.route('/widgets')
def get_widgets():
	mydb = conec.connect(host=chost, database = cdb, user = 'root', password=cpasswd)
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
	mydb = conec.connect(host=chost, user = 'root', password=cpasswd)
	cursor = mydb.cursor()

	cursor.execute("CREATE DATABASE IF NOT EXISTS pytcheck;")
	mydb= conec.connect(host=chost, database = cdb, user = 'root', password=cpasswd)
	cursor = mydb.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS widgets(name VARCHAR (255), description VARCHAR(255));")
	mydb.commit()
	return 'init database'


@app.route('/cleardb')
def db_clear():
        db = conec.connect(host=chost, database = cdb, user = 'root', password=cpasswd)
        cursor = db.cursor()

        cursor.execute("DROP TABLE widgets;")
        cursor.execute("CREATE TABLE widgets(name VARCHAR (255), description VARCHAR(255));")
        db.commit()
        return 'database cleared'

@app.route('/addvalues')
def add_values():
	db = conec.connect(host=chost, database = cdb, user = 'root', password=cpasswd)
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
	content = request.json
	_name = content["name"]
	_descript = content['description']
	con = conec.connect(host=chost, database = cdb, user = 'root', password=cpasswd)
	cursor = con.cursor()
	cursor.execute("INSERT INTO widgets VALUES('{}','{}');".format(_name,_descript))
	con.commit()
	return 'inserted'


if __name__ == "__main__":
	app.run(host = '0.0.0.0')

