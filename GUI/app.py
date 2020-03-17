import tkinter as tk
from bs4 import BeautifulSoup
import requests
from log_utilities import *

HEIGHT = 400
WIDTH = 800


titles = ['PART NAMES', "PART PICKED", "PRICE"]
parts = ['CPU', 'MOTHERBOARD', 'RAM', 'PSU', 'GPU', 'CASE', "DRIVE"]

grid_colors = ['#c4c4c4', '#e3e3e3']


def match(products, _search):
    _search = _search.lower()
    filtred_products = []
    for i in range(len(products)):
        filtred_products.append(str(products[i]).lower().replace('-', ''))
        if _search.replace(' ', '') in filtred_products[i]:
            print(products[i])


def get_price(soup):
    con = (str(soup.findAll(attrs={"name": "twitter:data1"}))).split()
    price = float((con[1][9:]).replace('.', '').replace(',', '.'))
    return price


def get_title(soup):
    return soup.title.text.replace(' - Skroutz.gr', '')


def get_search_url(search):
    return 'https://www.skroutz.gr/search?keyphrase=' + search.replace(' ', '+')


def update():
    total = 0
    for price in prices:
        try:
            total += float(price.get())
        except ValueError:
            continue
        label_price.config(text=f"{total}€")

    root.after(100, update)  # run itself again after 100 ms


def set_entries():
    l = load()
    for i in range(len(l[0])):
        names[i].delete(0,tk.END)
        prices[i].delete(0,tk.END)
        names[i].insert(0,l[0][i])
        prices[i].insert(0,l[1][i])

def refresh():
    entry = root.focus_get()
    print('hello')
    print(type(entry))


root = tk.Tk()
# root.resizable(width=False, height=False)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

main_frame = tk.Frame(root, bg='black')
main_frame.place(relwidth=0.75, relheight=1)

list_frame = tk.Frame(root, bg='grey')
list_frame.place(relx=0.75, relheight=1, relwidth=0.25)


# test_button = tk.Button(list_frame, bg='green',
#                         text='Refresh', command=refresh)
# test_button.pack(fill='x', side='bottom')



frame = tk.Frame(main_frame, bg='black')
frame.place(rely=0.1, relwidth=1, relheight=0.8)

# Titles
for i in range(len(titles)):
    label_title = tk.Label(main_frame, text=titles[i], bg='#91e3c4')
    label_title.place(relx=1/len(titles)*i, relwidth=1 /
                      len(titles), relheight=0.1,)

# Part Names
for i in range(len(parts)):
    label_part = tk.Label(frame, text=parts[i], bg=grid_colors[i % 2])
    label_part.place(rely=1/len(parts) * i,  relwidth=1 /
                     len(titles), relheight=1/len(parts))

prices = []
names = []
for i in range(len(titles)-1):
    for j in range(len(parts)):
        text = tk.Entry(frame, bg='white')
        text.place(relx=1/len(titles)*(i+1), rely=1/len(parts) * (j),
                   relwidth=1 / len(titles), relheight=1/len(parts))
        if i == 1:
            prices.append(text)
        elif i == 0:
            names.append(text)

label_total = tk.Label(main_frame, bg='#91e3c4', text="GRAND TOTAL")
label_total.place(rely=0.9, relwidth=0.5, relheight=0.1)

label_price = tk.Label(main_frame, bg='white', font=('Sans', 30))
label_price.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)

load_button = tk.Button(list_frame, text='Load', command= set_entries)
load_button.pack(side='bottom', fill='x')
save_button = tk.Button(list_frame, text='Save', command= lambda: save(format_log(parts,names,prices)))
save_button.pack(side='bottom', fill='x')

update()

root.mainloop()
