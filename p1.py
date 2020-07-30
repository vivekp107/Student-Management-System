from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import socket
import requests
import matplotlib.pyplot as plt
import numpy as np
import bs4
import requests

def f1():
	adst.deiconify()
	root.withdraw()
def f2():
	stdata.delete(1.0, END)
	vist.deiconify()
	root.withdraw()
	con = None
	try:
		con = connect("test.db")
		print("connected")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info =""
		for d in data:
			info = info + "rno: "+str(d[0])+" marks: " +str(d[1])+" name: "+ str(d[2]) + "\n"
		stdata.insert(INSERT, info)
	except Exception in e:
		print("select issue ",e)
	finally:
		if con is not None:
			con.close()
			print("disconnected")
def f3():
	upst.deiconify()
	root.withdraw()
def f4():
	dest.deiconify()
	root.withdraw()

def save():
	con = None
	try:
		con = connect("test.db")
		print("connected")
		rno = int(entrno.get())
		if rno < 0:
			showerror("failure" ,"invalid rno ")
			entrno.delete(0,END)
			entrno.focus()
			return
		name = entname.get()
		if len(name) < 2 or not name.isalpha() :
			showerror("failure" ,"invalid name ")
			entname.delete(0,END)
			entname.focus()
			return
		marks = int(entmarks.get())
		if marks < 0 or marks > 100:
			showerror("failure" ,"invalid range of marks ")
			entmarks.delete(0,END)
			entmarks.focus()
			return
		args = (rno , marks ,name )
		cursor = con.cursor()
		sql = "insert into student values('%d' ,'%d' ,'%s')"
		cursor.execute(sql % args)
		con.commit()
		showinfo("success" , "record added")			
	except Exception as e :
		showerror("failure", "Something Wrong " + str(e))
		con.rollback()	
	finally:
		if con is not None:
			con.close()
		entrno.delete(0,END)
		entrno.focus()
		entname.delete(0,END)
		entmarks.delete(0,END)
			
def back():
	root.deiconify()
	adst.withdraw()
def vback():
	root.deiconify()
	vist.withdraw()
def upsave():
	con = None		
	try:
		con = connect("test.db")
		print("connected")
		rno = int(entuprno.get())
		if rno < 0:
			showerror("failure" ,"invalid rno ")
			entuprno.delete(0,END)
			entuprno.focus()
			return
		name = entupname.get()
		if len(name) < 2 or not name.isalpha() :
			showerror("failure" ,"name shud be at least 2 letters ")
			entupname.delete(0,END)
			entupname.focus()
			return	
		marks = int(entupmarks.get())
		if marks < 0 or marks > 100:
			showerror("failure" ,"invalid range of marks ")
			entupmarks.delete(0,END)
			entupmarks.focus()
			return
		cursor = con.cursor()
		sql = "update student set marks=:1,name=:2 where rno=:3"
		cursor.execute(sql,(marks,name,rno))
		con.commit()
		if (cursor.rowcount==0):
			showerror("Galat kiya","Entered Roll No. is not present")
		else:
			showinfo("Successfull", str(cursor.rowcount) + "rows updated")
	except Exception as e :
		showerror("failure", "Something Wrong" + str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
		entuprno.delete(0,END)
		entuprno.focus()
		entupname.delete(0,END)	
		entupmarks.delete(0,END)

def upback():
	root.deiconify()
	upst.withdraw()
def desave():
	con = None
	try:
		con = connect("test.db")		
		rno = int(entderno.get())
		if rno < 0:
			showerror("Failure" ,"invalid rno ")
			entderno.delete(0,END)
			entderno.focus()
			return
		cursor = con.cursor()
		sql = "delete from student where rno=:rno "
		cursor.execute(sql,{"rno":rno})
		con.commit()
		if (cursor.rowcount==0):
			showerror("Galat kiya","Entered Roll No. is not present")
		else:
			showinfo("deleted", str(cursor.rowcount) + "row deleted")
	except DatabaseError as e:
		showerror("wrong kiya",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
		entderno.delete(0,END)
		entderno.focus()
def deback():
	root.deiconify()
	dest.withdraw()

def f5():
	marks=[]
	name=[]
	con=None
	try:
		con=connect("test.db")
		cursor=con.cursor()
		sql="select * from student order by marks desc"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			name.append(d[2]) 
			marks.append(d[1])


		gmarks=[marks[0],marks[1],marks[2]]
		gname=[name[0],name[1],name[2]]
		x=np.arange(len(gname))
		plt.bar(x,gmarks,label='marks out of 100')
		plt.xticks(x,gname)
		plt.xlabel('Names')
		plt.ylabel('Marks')
		plt.title("Top 3 students")
		plt.legend()
		plt.show()

	except DatabaseError as e:
		showerror("Error",e)
		con.rollback()
	except Exception as f:
		showerror("something is wrong","enter atleast 3 entries of students")
		con.rollback()
	finally:
		if con is not None:
			con.close()	

	

root = Tk()
root.title("S.M.S")
root.geometry("600x600+400+100")
root.resizable(False,False)


try:
	socket.create_connection(("www.google.com",80))
	print("you are connected")
	city="Mumbai"
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q="+ city
	a3="&appid=c6e315d09197cec231495138183954bd"
	api_address=a1+a2+a3
	res1=requests.get(api_address)
	print(res1)
	data=res1.json()
	main=data['main']
	temp_of_Mum=data['main']['temp']
	str1="   Mumbai                           "+str(temp_of_Mum)+"\u2103"

except OSError as e:
	print("check network",e)

try:
	res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
	print(res)
	soup=bs4.BeautifulSoup(res.text,'lxml')
	quote=soup.find('img',{"class":"p-qotd"})
	mesg=quote['alt']

except OSError as e:
	print("check network",e)



btnAdd = Button(root , text = "Add", width = 15, font=("arial",20,"bold"),command=f1)
btnView =Button(root , text = "View", width = 15, font=("arial",20,"bold"),command=f2)
btnUpdate = Button(root , text = "Update", width = 15, font=("arial",20,"bold"),command=f3)
btnDelete =Button(root , text = "Delete", width = 15, font=("arial",20,"bold"),command=f4)
btnCharts =Button(root , text = "Charts", width = 15, font=("arial",20,"bold"),command=f5)
lblTemp = Label(root,text=str1,font=("arial",20,"bold"),width=25)
lblQotd = Label(root,text=mesg,font=("arial",20,"bold"),wraplength=600)


btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnCharts.pack(pady=10)
lblTemp.place(x=5 , y=400)
lblQotd.place(x=10 , y=450)

#dessign of adst window --> Add student
adst = Toplevel(root)
adst.title("Add student")
adst.geometry("500x500+400+100")
adst.withdraw()

lblrno = Label(adst,text="Enter rno:",font=("arial",20,"bold"))
entrno = Entry(adst, bd=5 ,font=("arial",20,"bold"))
lblname = Label(adst,text="Enter name:",font=("arial",20,"bold"))
entname = Entry(adst, bd=5 ,font=("arial",20,"bold"))
lblmarks = Label(adst,text="Enter marks:",font=("arial",20,"bold"))
entmarks = Entry(adst, bd=5 ,font=("arial",20,"bold"))
btnsave = Button(adst,text="Save",font=("arial",20,"bold"),command=save)
btnback = Button(adst,text="Back",font=("arial",20,"bold"),command = back)


lblrno.pack(pady=5)
entrno.pack(pady=5)
lblname.pack(pady=5)
entname.pack(pady=5)
lblmarks.pack(pady=5)
entmarks.pack(pady=5)
btnsave.pack(pady=5)
btnback.pack(pady=5)


#design of vist window --> view data

vist = Toplevel(root)
vist.title("View St.")
vist.geometry("500x500+400+100")
vist.withdraw()

stdata = ScrolledText(vist,width=50,height=25)
btnvback = Button(vist,text="Back",font=("arial",20,"bold"),command = vback)

stdata.pack(pady=10)
btnvback.pack(pady=10)


#design of upst window --> update student
upst = Toplevel(root)
upst.title("Update St.")
upst.geometry("500x500+400+100")
upst.withdraw()

lbluprno = Label(upst,text="Enter rno:",font=("arial",20,"bold"))
entuprno = Entry(upst, bd=5 ,font=("arial",20,"bold"))
lblupname = Label(upst,text="Enter name:",font=("arial",20,"bold"))
entupname = Entry(upst, bd=5 ,font=("arial",20,"bold"))
lblupmarks = Label(upst,text="Enter marks:",font=("arial",20,"bold"))
entupmarks = Entry(upst, bd=5 ,font=("arial",20,"bold"))
btnupsave = Button(upst,text="Save",font=("arial",20,"bold"),command=upsave)
btnupback = Button(upst,text="Back",font=("arial",20,"bold"),command=upback)


lbluprno.pack(pady=5)
entuprno.pack(pady=5)
lblupname.pack(pady=5)
entupname.pack(pady=5)
lblupmarks.pack(pady=5)
entupmarks.pack(pady=5)
btnupsave.pack(pady=5)
btnupback.pack(pady=5)


#design of dest window --> delete student

dest = Toplevel(root)
dest.title("Delete St.")
dest.geometry("500x500+400+100")
dest.withdraw()

lblderno = Label(dest,text="Enter rno:",font=("arial",20,"bold"))
entderno = Entry(dest, bd=5 ,font=("arial",20,"bold"))
btndesave = Button(dest,text="Save",font=("arial",20,"bold"),command=desave)
btndeback = Button(dest,text="Back",font=("arial",20,"bold"),command=deback)

lblderno.pack(pady=5)
entderno.pack(pady=5)
btndesave.pack(pady=5)
btndeback.pack(pady=5)




root.mainloop()