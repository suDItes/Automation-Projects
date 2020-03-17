import tkinter as tk

HEIGHT = 400
WIDTH = 600


titles = ['PART NAMES', "PART PICKED", "PRICE"]
parts = ['CPU', 'MOTHERBOARD', 'RAM', 'PSU', 'GPU', 'CASE', "DRIVE"]

grid_colors = ['#c4c4c4', '#e3e3e3']


def update():
    total = 0
    for price in prices:
        try:
            total += float(price.get())
        except ValueError:
            continue
        label_price.config(text= f"{total}€")
    root.after(100, update)  # run itself again after 1000 ms


root = tk.Tk()
# root.resizable(width=False, height=False)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='black')
frame.place(rely=0.1, relwidth=1, relheight=0.8)

# Titles
for i in range(len(titles)):
    label_title = tk.Label(root, text=titles[i], bg='#91e3c4')
    label_title.place(relx=1/len(titles)*i, relwidth=1 /
                      len(titles), relheight=0.1,)

# Part Names
for i in range(len(parts)):
    label_part = tk.Label(frame, text=parts[i], bg=grid_colors[i % 2])
    label_part.place(rely=1/len(parts) * i,  relwidth=1 /
                     len(titles), relheight=1/len(parts))


prices = []
for i in range(len(titles)-1):
    for j in range(len(parts)):
        text = tk.Entry(frame, bg='white')
        text.place(relx=1/len(titles)*(i+1), rely=1/len(parts) * (j),
                   relwidth=1 / len(titles), relheight=1/len(parts))
        if j <= len(parts)-1:
            prices.append(text)

label_total = tk.Label(root, bg='#91e3c4', text="GRAND TOTAL")
label_total.place(rely=0.9, relwidth=0.5, relheight=0.1)

label_price = tk.Label(root, bg='white', font=('Sans', 30))
label_price.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)

update()

root.mainloop()
