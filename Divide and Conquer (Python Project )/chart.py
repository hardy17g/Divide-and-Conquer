from tkinter import *
import database
import pandas as pd
import matplotlib.pyplot as plt
import tkinter.messagebox
def chart_display():
	root= Toplevel()
	global yo
	global po
	global mo
	yo = IntVar()
	po = IntVar()
	mo = IntVar()

	y=Checkbutton(root,text="Yearly",variable = yo)
	y.grid(row=0,column=0)
	y1=Label(root,text="YEAR")
	y1_entry=Entry(root)

	y1.grid(row=1,column=0)
	y1_entry.grid(row=1,column=1)

	#MONTHLY
	m=Checkbutton(root,text="Monthly(Day wise)",variable = mo)
	m.grid(row=0,column=2)

	monYear1=Label(root,text="YEAR"	)
	monYear1_entry=Entry(root)

	monYear1.grid(row=1,column=2)
	monYear1_entry.grid(row=1,column=3)

	monMONTH1=Label(root,text="MONTH")
	monMONTH1_entry=Entry(root)

	monMONTH1.grid(row=2,column=2)
	monMONTH1_entry.grid(row=2,column=3)

	#MONTHLY CATEG
	m2=Checkbutton(root,text="Monthly(CATEGORY WISE)",variable = po)
	m2.grid(row=0,column=4)

	monYear2=Label(root,text="YEAR"	)
	monYear2_entry=Entry(root)

	monYear2.grid(row=1,column=4)
	monYear2_entry.grid(row=1,column=5)

	monMONTH2=Label(root,text="MONTH"	)
	monMONTH2_entry=Entry(root)

	monMONTH2.grid(row=2,column=4)
	monMONTH2_entry.grid(row=2,column=5)
	# plotting data
	def display_data(month,year):
		arr = database.return_month_data(month,year)
		if arr != None:
			arr = pd.DataFrame(arr,columns = ['Date','Amount'])
			arr.plot(kind='bar',x='Date',y='Amount',color='blue')
			plt.show()
		else:
			tkinter.messagebox.showinfo("ERROR", "NO ENTRY FOR THE GIVEN MONTH")
			#print("ERROR: NO ENTRY FOR THE GIVEN MONTH")
	def display_year_data(year):
		arr = database.return_year_data(year)
		if arr != None:
			arr = pd.DataFrame(arr,columns = ['Month','Amount'])
			arr.plot(kind='bar',x='Month',y='Amount',color='green')
			plt.show()
		else :
			tkinter.messagebox.showinfo("ERROR", "NO ENTRY FOR THE GIVEN YEAR")	
	def display_category_pie(month,year):
		arr = database.return_category_expenditure(month,year)
		if arr!=None:
			arr = pd.DataFrame(arr,columns = ['Category','Amount'])
			category = arr.Category
			lbls = list(category)
			amount = list(arr['Amount'])
			plt.pie(amount,labels = lbls, autopct = '%.2f')
			plt.show()
		else:
			tkinter.messagebox.showinfo("ERROR", "NO ENTRY FOR THE GIVEN MONTH")
	def submit():
		if yo.get() == 1:
			display_year_data(y1_entry.get())
		if po.get() == 1:
			display_category_pie(monMONTH2_entry.get(),monYear2_entry.get())
		if mo.get()	== 1:
			display_data(monMONTH1_entry.get(),monYear1_entry.get())
		root.destroy()

	submit=Button(root,text="SUBMIT",fg="red",command = submit)

	submit.grid(row=6,column=3)


	root.mainloop()