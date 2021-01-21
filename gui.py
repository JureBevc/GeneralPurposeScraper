from tkinter import *

window = Tk()
window.geometry("350x400")
window.title("General Purpose Scraper")


url_lbl = Label(window, text="Url:")
url_lbl.grid(column=0,row=0)
url_txt = Entry(window,width=40)
url_txt.grid(column=1, row=0, sticky=E+W+N+S)

go_btn = Button(window, text="Go!", width=5, height=3)
go_btn.grid(column=1, row=1)

window.mainloop()