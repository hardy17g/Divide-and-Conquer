import client
from client import *
import threading
import queue
from queue import *
import json
import database
import pandas as pd
import tkinter
from tkinter import *
import tkinter.messagebox
import matplotlib.pyplot as plt
months = {'1':"January",'2':"February",'3':"March",'4':"April",'5':"May",'6':"June",'7':"July",'8':"August",'9':"September",'10':"October",'11':"November",'12':"December"}
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
f2 = open("user.txt",'r')
user = f2.read()
f2.close()
def main_window():
	import add_expense
	import chart
	root=Tk()
	tkinter.messagebox.showinfo('DIVIDE AND CONQUER',"WELCOME!" )
	def daily_exp():
		r = Toplevel()
		label = Label(r,text = 'Enter Date:')
		label.pack()
		e1 = Entry(r)
		e1.pack()
		def submit():
			global txt
			txt.destroy()
			txt = Text(r)
			txt.pack()
			day,month,year = tuple(e1.get().split(':'))
			data = f"For {day} {months[month]}, {year}:\n" 
			x =database.get_date_expenses(day,month,year)[0]
			if x[0] =='E':
				data+= 'No entry for the date!'
			else:
				data += x
			#txt.config(state = 'disabled')
			txt.insert(INSERT,data)
		global txt
		txt = Text(r)
		txt.pack()
			
		b1 = Button(r,text = 'SUBMIT', command = submit)
		b1.pack()
		r.mainloop()
	def current_status():
		for x in lbls1:
			x.configure(text = '')
		for x in lbls2:
			x. configure(text= '')	
		f = open("user_split.txt",'r')
		sd = json.loads(f.read())
		f.close()
		for i,x in enumerate(sd['returnFrom'].keys()):
			bal = sd['returnFrom'][x] - sd['owedTo'][x]
			if bal > 0:
				lbls1[i].configure(text = f'You get back Rs. {bal} from {x}')
				lbls1[i].update()
			if bal < 0:
				lbls2[i].configure(text = f'You owe Rs. {-bal} to {x}')
				lbls2[i].update()
			if bal == 0:
				tkinter.messagebox.showinfo('Congratulations!',f"You are settled with {x}")
		
		'''if len(sd["returnFrom"].keys())!=0:	
			pic1=PhotoImage(file="split.png")
			lb=Label(root,image=pic1)
			lb.pack()
		else:
			pic1=PhotoImage(file="champagne.png")
			lb=Label(root,image=pic1)
			lb.pack()'''
		
	def add_exp():
		add_expense.add_expense_f()	
	def graph():
		chart.chart_display()
	pic=PhotoImage(file="logo.png")
	lbl=Label(root,image=pic)
	lbl.pack()
	b1=Button(root,text='ADD EXPENSE',command=add_exp)
	b1.pack()
	b4 = Button(root,text='DAILY EXPENDITURE',command=daily_exp)
	b4.pack()
	b2=Button(root,text='VIEW GRAPHS',command=graph)
	b2.pack()
	b3=Button(root,text='YOUR CURRENT STATUS',command=current_status)
	b3.pack()
	l1 = Label(root,text = '')
	l1.pack()
	l2 = Label(root, text = '')
	l2.pack()
	lbls1 = [l1,l2]
	l3 = Label(root,text = '')
	l3.pack()
	l4 = Label(root, text = '')
	l4.pack()
	lbls2 = [l3,l4]
	root.mainloop()
	
def update_query(d):
	#del d['user']
	database.log(**d)
temp = {}
def work():
    global temp
    while True:
        d = client.receive_string(user)
        if(d!=None):
            if temp != d:	
                print(d)
                update_query(d)
                temp = d
t = threading.Thread(target=work)
t.daemon = True
t.start()       
main_window()

