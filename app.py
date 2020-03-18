import tkinter as tk
from bs4 import BeautifulSoup
import requests
from log_utilities import *

HEIGHT = 400
WIDTH = 800


titles = ['PART NAMES', "PART PICKED", "PRICE"]
parts = ['CPU', 'MOTHERBOARD', 'RAM', 'PSU', 'GPU', 'CASE', "DRIVE"]

grid_colors = ['#c4c4c4', '#e3e3e3']

global last_entry
product_urls = []


def match(products, _search):
    _search = _search.lower()
    filtred_products = []
    for i in range(len(products)):
        filtred_products.append(str(products[i]).lower().replace('-', ''))
        if _search.replace(' ', '') in filtred_products[i]:
            position1 = filtred_products[i].find("/")
            position2 = filtred_products[i].find(("/"), position1+1)
            position3 = filtred_products[i].find(("/"), position2+1)
            products[i] = filtred_products[i][position3:]
            products[i] = filtred_products[i][position3+1:-5]
            print(products[i])


# return price given the url end
def get_price(url):
    url = 'https://www.skroutz.gr' + url
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    con = (str(soup.findAll(attrs={"name": "twitter:data1"}))).split()
    price = float((con[1][9:]).replace('.', '').replace(',', '.'))
    return price


# Get page title
def get_title(soup):
    return soup.title.text.replace(' - Skroutz.gr', '')


# Clean URL
def get_name(url):
    start = url.rfind('/')+1
    name = url[start:-5]
    name = name.replace('-', ' ')
    return name


# returns Search url for given search
def get_search_url(search):
    return 'https://www.skroutz.gr/search?keyphrase=' + search.replace(' ', '+')


# Auto-update Total Price
def update():
    total = 0
    for price in prices:
        try:
            total += float(price.get())
        except ValueError:
            continue
        label_price.config(text="%.2f€" % total)

    root.after(100, update)  # run itself again after 100 ms


# Load function call
def set_entries():
    l = load()
    for i in range(len(l[0])):
        names[i].delete(0, tk.END)
        prices[i].delete(0, tk.END)
        names[i].insert(0, l[0][i])
        prices[i].insert(0, l[1][i])


# Called when an element of the list is selected
def autocomplete(event):
    w = event.widget
    ind = int(w.curselection()[0])
    global last_entry
    ent_ind = names.index(last_entry)
    last_entry.delete(0, tk.END)
    last_entry.insert(0, w.get(ind))
    prices[ent_ind].delete(0, tk.END)
    prices[ent_ind].insert(0, get_price(product_urls[ind]))


# Search for results in skroutz.gr
def refresh():
    global last_entry
    last_entry = root.focus_get()
    if last_entry in names:
        search = last_entry.get()
        print(search)
        search_url = get_search_url(search)
        page = requests.get(search_url)
        search_soup = BeautifulSoup(page.text, 'lxml')
        products = search_soup.findAll('a', attrs={'class': 'js-sku-link image_link'})
        products.extend(search_soup.findAll('a', attrs={'class': 'js-sku-link pic'}))
        product_urls.clear()
        for p in products:
            product_urls.append(p.get('href'))
        product_list.delete(0,tk.END)
        for p in product_urls:
            product_list.insert(tk.END, get_name(p))


root = tk.Tk()
# root.resizable(width=False, height=False)

root.title("SUDI Part Picker")

# Window size initialization
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Main frame
main_frame = tk.Frame(root, bg='black')
main_frame.place(relwidth=0.75, relheight=1)

# Frame for list and buttons
list_frame = tk.Frame(root, bg='grey')
list_frame.place(relx=0.75, relheight=1, relwidth=0.25)

# ~~~~~ BUTTONS ~~~~~ #
# Load button
load_button = tk.Button(list_frame, text='Load', command=set_entries)
load_button.pack(side='bottom', fill='x')
# Save button
save_button = tk.Button(list_frame, text='Save',
                        command=lambda: save(format_log(parts, names, prices)))
save_button.pack(side='bottom', fill='x')
# Search button
search_button = tk.Button(list_frame, bg='pink',
                          text='Search', command=refresh)
search_button.pack(fill='x', side='bottom')
# ~~~~~~~~~~~~~~~~~~~ #

# Scrollbar
scroll = tk.Scrollbar(list_frame)
scroll.pack(side='right', fill='y')
# Search result product list
product_list = tk.Listbox(list_frame, yscrollcommand=scroll.set)
product_list.bind('<<ListboxSelect>>', autocomplete)
product_list.pack(side='left', fill='both', expand='True')
scroll.config(command=product_list.yview)

# Frame for entries
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

# Entries
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

# Total price
label_total = tk.Label(main_frame, bg='#91e3c4', text="GRAND TOTAL")
label_total.place(rely=0.9, relwidth=0.5, relheight=0.1)
label_price = tk.Label(main_frame, bg='white', font=('Sans', 30))
label_price.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)


update()

root.mainloop()
