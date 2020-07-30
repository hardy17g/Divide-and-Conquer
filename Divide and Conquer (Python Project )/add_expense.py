from tkinter import *
import tkinter.font
import database
from datetime import datetime
import client
import json
#import time
#import client
def add_expense_f():
	global root1
	global f
	global t
	global l
	global life
	global h
	global j
	global u
	def submit():

		date=e1.get()
		expense=float(e3.get())
		description=e4.get()
		c = []
		category = ''
		if h.get() == 1:
			c.append("Hardik")
		if j.get()==1:
			c.append("Jaideep")	
		if u.get() ==1:
			c.append("Utkarsh")
		if f.get() ==1:
			category='Food'
		if t.get() ==1:
			category='Transport'
		if l.get() ==1:
			category='Leisure'
		if life.get() ==1:
			category='Lifestyle'
		day,month,year = tuple(date.split(":"))
		n = datetime.now()
		ti = n.strftime("%H:%M:%S")
		fl = open("user.txt",'r')
		user = fl.read()
		fl.close()
		split = 0.0
		sd = {}
		if len(c)!=0:
			send_str = {}
			list_send = []
			sd = {"user":user,"returnFrom":{},"owedTo":{}}
			le = len(c)
			if sd["user"] in c:
				split = -(expense/len(c))*(len(c)-1)
				c.remove(sd['user'])
				for x in c:
					sd["returnFrom"][x] = expense/le
			else:
				split = -expense
				for x in c:
					sd["returnFrom"][x] = expense/le
			for x in sd["returnFrom"].keys():
				send_str = {"user":x,"day":day,"month":month,"year":year,"time":ti,"expen":float(sd["returnFrom"][x]),"split":0,"cat":category,"split_dictionary":{"user":x,"returnFrom":{},"owedTo":{sd["user"]:sd["returnFrom"][x]}},"comments":description} 
				list_send.append(send_str)
			client.send_string(json.dumps(list_send))
			#time.sleep(2)
			print(json.dumps(list_send))


		database.log(user,day,month,year,ti,expense,split,category,sd,description)
		#print(f"{day},{month},{year} ,{category} ,{expense} ,{description},{ti},{split},{sd} ")
		root1.destroy()
	def split_exp():
		global h
		global j
		global u
		l=Label(root1,text='SPLIT WITH:')
		l.grid(row=6,sticky=E)
		c1=Checkbutton(root1,text='HARDIK',variable = h)
		c1.grid(row=6,column=1)
		c2=Checkbutton(root1,text='JAIDEEP',variable = j)
		c2.grid(row=6,column=2)
		c3=Checkbutton(root1,text='UTKARSH',variable = u)
		c3.grid(row=6,column=3)
	def category_select():
		global f
		global t
		global l
		global life
		l2=Label(root1,text='CHOOSE CATEGORY')
		l2.grid(row=1,sticky=E)
		c1=Checkbutton(root1,text='FOOD',variable = f)
		c1.grid(row=1,column=1,sticky=W)
		c2=Checkbutton(root1,text='TRANSPORT',variable = t)
		c2.grid(row=1,column=2,sticky=W)
		c3=Checkbutton(root1,text='LEISURE',variable = l)
		c3.grid(row=2,column=1,sticky=W)
		c4=Checkbutton(root1,text='LIFESTYLE',variable = life)
		c4.grid(row=2,column=2,sticky=W)	

	root1=Toplevel()
	label1=Label(root1,text='DATE')
	label1.grid(row=0, sticky=E)

	label3=Label(root1,text='EXPENSE')
	label3.grid(row=3, sticky=E)
	label4=Label(root1,text='DESCRIPTION')
	label4.grid(row=4, sticky=E)
	e1=Entry(root1)
	e1.grid(row=0,column=1)

	e3=Entry(root1)
	e3.grid(row=3,column=1)
	e4=Entry(root1)
	e4.grid(row=4,column=1)
	h = IntVar()
	j = IntVar()
	u = IntVar()
	b2=Button(root1,text='SPLIT EXPENSE',command=split_exp)
	b2.grid(row=5,columnspan=3)
	f = IntVar()
	t = IntVar()
	l = IntVar()
	life=IntVar()


	b1=Button(root1,text='SUBMIT',command=submit)
	b1.grid(row=7,columnspan=3)
	category_select()
	root1.mainloop()



