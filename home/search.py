from tkinter import *
import webbrowser
from tkinter import Entry

root = Tk()

root.title("search tab")

def search():
    url=entry.get()
    webbrowser.open(url)

label1=Label(root,text="Enter Movie Title", font=("Arial", 20))
label1.grid(row=0, column=0)

entry=Entry(root,width=30)
entry.grid(row=0, column=1)

button=Button(root,text="Search",command=search)

button.grid(row=1, column=0, columnspan=2,pady=10)

root.mainloop()