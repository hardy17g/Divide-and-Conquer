import sqlite3
import json
from sqlite3 import *
import pandas as pd
months = {'1':"January",'2':"February",'3':"March",'4':"April",'5':"May",'6':"June",'7':"July",'8':"August",'9':"September",'10':"October",'11':"November",'12':"December"}
def log(user,day,month,year,time,expen,split,cat,split_dictionary,comments=""):
	f = open("years.txt",'r')
	years = json.loads(f.read())
	f.close()
	f = open("user_split.txt",'r')
	sd = json.loads(f.read())
	f.close()
	if len(split_dictionary.keys())>0:
		if split!=0:
			for x in split_dictionary["returnFrom"].keys():
				if x not in sd["returnFrom"]:
					sd["returnFrom"][x] = 0
				sd['returnFrom'][x]+=split_dictionary["returnFrom"][x]
			print(sd)
			f = open("user_split.txt",'w')
			f.write(json.dumps(sd))
			f.close()
		elif len(split_dictionary["owedTo"].keys())>0:
			for x in split_dictionary["owedTo"].keys():
				if x not in sd["owedTo"]:
					sd["owedTo"][x] = 0
				sd['owedTo'][x]+=split_dictionary["owedTo"][x]
			f = open("user_split.txt",'w')
			f.write(json.dumps(sd))
			f.close()	

	mydb = connect("expenses.db")
	mycursor=mydb.cursor()
	if year not in years:
		years[year] = {}
		years[year][month] = expen+split
	else:
		if month not in years[year]:
			years[year][month] = 0
		years[year][month] += expen+split
	f = open("years.txt",'w')
	f.write(json.dumps(years))
	f.close()
	print(years)
	query = "create table if not exists {}(day VARCHAR(2), tm VARCHAR(10),expense DECIMAl(10,2) ,split DECIMAl(10,2) ,category VARCHAR(20) ,comments VARCHAR(255),year VARCHAR(4), PRIMARY KEY(day,tm))".format(months[month])
	mycursor.execute(query)
	mydb.commit()
	print("inserting into {}".format(months[month]))
	query="INSERT INTO {}(day,tm,expense,split,category,comments,year)	VALUES (?,?,?,?,?,?,?)".format(months[month])
	ent=(day,time,expen,split,cat,comments,year)
	mycursor.execute(query,ent)
	mydb.commit()
	print("Inserted")
def get_date_expenses(day,month,year):
	mydb = connect("expenses.db")
	mycursor = mydb.cursor()
	try:
		r_count = mycursor.execute("select tm,expense,split,(expense+split),category,comments from {} where year = {} and day = {}".format(months[month],year, day))
		result = mycursor.fetchall()
		x =  pd.DataFrame(result, columns = ['Time','Expense','Split','Amount','Category','Comments'])
		return x.to_string()
	except:
		return None
def return_month_data(month,year):
	mydb = connect("expenses.db")
	mycursor = mydb.cursor()
	try:
		result = mycursor.execute("select day,sum(expense+split) from {} where year = {} group by day".format(months[month],year))
		result = mycursor.fetchall()
		return result
	except:
		return None
		#print("Error")	
	
def return_category_expenditure(month,year):
	mydb = connect("expenses.db")
	mycursor = mydb.cursor() 
	try:
		result = mycursor.execute("select category , sum(expense+split) from {} where year = {} group by category order by category".format(months[month],year))
		result = mycursor.fetchall()
		return result
	except:
		return None
		#print("Error")

def return_year_data(year):
	f = open("years.txt",'r')
	years = json.loads(f.read())
	f.close()
	if year not in years:
		#print("No entry for the given year")
		return None
	else:
		return list(years[year].items())
		#print(list(years[year].items()))
'''mydb = connect("expenses.db")
mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS November")
mydb.commit()
'''
'''	
log('10','11','2019',"12:05:45",270,0,"Food",{},"Boba Drinks")
log('10','11','2019',"12:06:45",600,-400,"Food",{"user":"Utkarsh","returnFrom":{"Hardik":200,"Jaideep":200},"owedTo":{}},"Boba Drinks")
log('12','11','2019',"12:05:45",500,0,"Transport",{},"Uber")
#return_category_expenditure('11','2019')
return_month_data('11','2019')
#return_year_data('2019')
'''
