from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import threading
import time
from general_scraper.scraper import Scraper
from general_scraper.extractor import Extractor

bg_color = "#FFF8F0"
text_color = "#0C0C0C"
btn_go_color = "#329F5B"
btn_stop_color = "#BA3B46"

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
    status_lbl["text"] = "Status (STOPPED):\nScraper ready."

def stop_scraper_method():
    global scraper, go_btn
    if scraper:
        scraper.stop()
    go_btn["state"] = ACTIVE

def print_status(status):
    global status_lbl, start_scraper, scraper, go_btn
    if start_scraper:
        go_btn["state"] = ACTIVE
        status_lbl["text"] = "Status (RUNNING):\n" + """
Elapsed time: {} s
Queue size: {}
Visited: {}
Extracted: {}
Saved: {}
        """.format(status["elapsed_time"], status["queue_size"], status["visited"],
        status["extracted"], status["saved"])
    else:
        status_lbl["text"] = "Status (STOPPING):\nStopping {} crawlers...".format(scraper.alive_count())

def toggle_button():
    global start_scraper, go_btn, status_lbl, xpath_txt, url_txt, limit_txt, threads_txt, html_is_checked, status_lbl, file_txt
    global extract, scraper, scraper_thread, btn_go_color, btn_stop_color
    start_scraper = not start_scraper 
    if start_scraper:
        if scraper_thread:
            scraper_thread.join()
        
        extract = Extractor(xpath_txt.get(), extract_as_html=html_is_checked.get() == 1, output_file=file_txt.get())
        url_match = list(filter(None, limit_txt.get("1.0", END).split("\n")))
        starting_urls = list(filter(None, url_txt.get("1.0", END).split("\n")))
        scraper = Scraper(starting_urls, extract, url_match=url_match, thread_count=int(threads_txt.get()), status_callback=print_status)

        scraper_thread = threading.Thread(target=scraper_thread_method)
        scraper_thread.daemon = True
        scraper_thread.start()

        go_btn["state"] = DISABLED
        go_btn["text"] = "Stop"
        go_btn["bg"] = btn_stop_color
        status_lbl["text"] = "Status (RUNNING):\nStarting {} crawlers.".format(scraper.thread_count)
    else:
        stop_scraper_thread = threading.Thread(target=stop_scraper_method)
        stop_scraper_thread.daemon = True
        stop_scraper_thread.start()
        status_lbl["text"] = "Status (STOPPING):\nStopping {} crawlers ...".format(scraper.thread_count)
        go_btn["state"] = DISABLED
        go_btn["text"] = "Go!"
        go_btn["bg"] = btn_go_color

def only_numbers(char):
    return char.isdigit()

window = Tk()
window.iconbitmap("res/icon.ico")
window.geometry("800x600")
window.title("General Purpose Scraper")
window.configure(bg=bg_color)
only_numbers_command = window.register(only_numbers)

url_lbl = Label(window, text="Starting URLs:", bg=bg_color,fg=text_color, font="bold")
url_lbl.pack(side=TOP)
url_txt = scrolledtext.ScrolledText(window, undo=True, height=6)
url_txt.pack(side=TOP)
url_txt.insert(INSERT, "https://twitter.com/slovenija")

ttk.Separator(window, orient=HORIZONTAL).pack(side=TOP, fill="x")
limit_lbl = Label(window, text="Limit to URLs:", bg=bg_color,fg=text_color, font="bold")
limit_lbl.pack(side=TOP)
limit_txt = scrolledtext.ScrolledText(window, undo=True, height=6)
limit_txt.pack(side=TOP)
limit_txt.insert(INSERT, "twitter.com\nwww.twitter.com")

ttk.Separator(window, orient=HORIZONTAL).pack(side=TOP, fill="x")
xpath_lbl = Label(window, text="XPath expression:", bg=bg_color,fg=text_color, font="bold")
xpath_lbl.pack(side=TOP)
xpath_txt = Entry(window, width=100, justify="center")
xpath_txt.pack(side=TOP)
xpath_txt.insert(0, "//div[@data-testid='tweet' and contains(string(), 'covid')]")

ttk.Separator(window, orient=HORIZONTAL).pack(side=TOP, fill="x")
threads_lbl = Label(window, text="Scraper threads:", bg=bg_color,fg=text_color, font="bold")
threads_lbl.pack(side=TOP)
threads_txt = Entry(window, width=5, justify="center", validate="all", validatecommand=(only_numbers_command, "%S"))
threads_txt.pack(side=TOP)
threads_txt.insert(0, "3")

html_is_checked = IntVar()
extract_html_check = Checkbutton(window, text="Extract as html", bg=bg_color, font="bold", variable=html_is_checked)
extract_html_check.pack(side=TOP)

file_frame = Frame(window, width=100, bg=bg_color)
file_frame.pack(side=TOP)
file_lbl = Label(file_frame, text="Output file:", bg=bg_color,fg=text_color, font="bold")
file_lbl.pack(side=LEFT)
file_txt = Entry(file_frame, width=50, justify="center")
file_txt.pack(side=LEFT)
file_txt.insert(0, "extracted.txt")

ttk.Separator(window, orient=HORIZONTAL).pack(side=TOP, fill="x")
ttk.Separator(window, orient=HORIZONTAL).pack(side=TOP, fill="x")

status_lbl = Label(window, text="", bg=bg_color,fg=text_color, font="Tahoma 12 bold", justify="center")
status_lbl.pack(side=TOP)
status_lbl["text"] = "Status:\nScraper ready to start."


go_btn = Button(window, text="Go!", width=5, height=1, bg=btn_go_color, fg=text_color, font="Tahoma 15 bold", command=toggle_button)
go_btn.pack(side=BOTTOM)

thread = threading.Thread(target=scraper_thread)
thread.daemon = True

window.mainloop()