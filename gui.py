from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import threading
import time
from general_scraper.scraper import Scraper
from general_scraper.extractor import Extractor

bg_color = "#f4f1de"



extract = None
scraper = None
scraper_thread = None
start_scraper = False

def scraper_thread_method():
    global extract, scraper
    try:
        scraper.start()
    except Exception as e:
        print(e)
        scraper.stop()
    status_lbl["text"] = "Status (STOPPED):\n"

def print_status(text):
    global status_lbl, start_scraper
    status_lbl["text"] = "Status(" + ("RUNNING" if start_scraper else "STOPPING") + "):\n" + str(text)

def toggle_button():
    global start_scraper, go_btn, status_lbl, xpath_txt, url_txt, limit_txt, threads_txt, extract_html_check, status_lbl
    global extract, scraper, scraper_thread
    start_scraper = not start_scraper 
    if start_scraper:
        if scraper_thread:
            scraper_thread.join()
        
        extract = Extractor(xpath_txt.get())
        url_match = list(filter(None, limit_txt.get("1.0", END).split("\n")))
        starting_urls = list(filter(None, url_txt.get("1.0", END).split("\n")))
        scraper = Scraper(starting_urls, extract, url_match=url_match, thread_count=int(threads_txt.get()), status_callback=print_status)

        scraper_thread = threading.Thread(target=scraper_thread_method)
        scraper_thread.daemon = True
        scraper_thread.start()

        go_btn["text"] = "Stop"
        go_btn["bg"] = "#e07a5f"
        status_lbl["text"] = "Status (RUNNING):\n"
    else:
        scraper.stop()
        go_btn["text"] = "Go!"
        go_btn["bg"] = "#81b29a"
        status_lbl["text"] = "Status (STOPPING):\n"

def only_numbers(char):
    return char.isdigit()

window = Tk()
window.geometry("500x600")
window.title("General Purpose Scraper")
window.configure(bg=bg_color)
only_numbers_command = window.register(only_numbers)

url_lbl = Label(window, text="Starting URLs:", bg=bg_color,fg="#121113", font="bold")
url_lbl.pack(side=TOP)
url_txt = scrolledtext.ScrolledText(window, undo=True, height=6)
url_txt.pack(side=TOP)
url_txt.insert(INSERT, "https://twitter.com/slovenija")

limit_lbl = Label(window, text="Limit URLs:", bg=bg_color,fg="#121113", font="bold")
limit_lbl.pack(side=TOP)
limit_txt = scrolledtext.ScrolledText(window, undo=True, height=6)
limit_txt.pack(side=TOP)
limit_txt.insert(INSERT, "https://twitter.com\nhttps://www.twitter.com")

xpath_lbl = Label(window, text="XPath expression:", bg=bg_color,fg="#121113", font="bold")
xpath_lbl.pack(side=TOP)
xpath_txt = Entry(window, width=100, justify="center")
xpath_txt.pack(side=TOP)
xpath_txt.insert(0, "//div[@data-testid='tweet' and (contains(string(), 'covid') or contains(string(), 'korona'))]")

threads_lbl = Label(window, text="Scraper threads:", bg=bg_color,fg="#121113", font="bold")
threads_lbl.pack(side=TOP)
threads_txt = Entry(window, width=5, justify="center", validate="all", validatecommand=(only_numbers_command, "%S"))
threads_txt.pack(side=TOP)
threads_txt.insert(0, "3")

extract_html_check = Checkbutton(window, text="Extract as html", bg=bg_color, font="bold")
extract_html_check.pack(side=TOP)

ttk.Separator(window, orient=HORIZONTAL).pack(side=TOP, fill="x")

status_lbl = Label(window, text="", bg=bg_color,fg="#000000", font="Tahoma 12 bold", justify="center")
status_lbl.pack(side=TOP)
status_lbl["text"] = "Status:\nScraper ready to start."

ttk.Separator(window, orient=HORIZONTAL).pack(side=TOP, fill="x")

go_btn = Button(window, text="Go!", width=5, height=1, bg="#81b29a", fg="#F8F7FF", font="Tahoma 15 bold", command=toggle_button)
go_btn.pack(side=BOTTOM)

thread = threading.Thread(target=scraper_thread)
thread.daemon = True

window.mainloop()