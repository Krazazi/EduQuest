
from tkinter import *
from tkinter import messagebox
import random
import pyodbc
from PIL import Image, ImageTk

w = Tk()
w.title("Pexeso")
w.configure(bg="#f7f3e9")  # Jemná pastelová barva pozadí
w.geometry("800x400")
w.resizable(False, False)

font = ("Helvetica", 12, "bold")

w2 = None
name = None
agree = None

with open("login.txt", "r") as login:
    name = login.readline()
    if name == "":
        name = "Login"
def main_pexeso(soubor, num):
    global w2
    pary = {}
    cursor.execute(f'SELECT * FROM {soubor};')
    l = cursor.fetchall()
    for x in range(0, 16, 2):
        pary.update({f"{l[x][0]}": f"{l[x+1][0]}"})

    pary.update({v: k for k, v in pary.items()})

    if num == 1:
        w2 = Toplevel(w)
        w2.configure(bg="#f7f3e9")

    slova = list(pary.keys())
    random.shuffle(slova)

    buttons = []
    b1 = -1
    text1 = None

    def reset_buttons(b, b2):
        nonlocal b1
        buttons[b].config(bg="lavender")
        buttons[b2].config(bg="lavender")
        b1 = -1

    def pexeso(btn, index):
        nonlocal b1, text1
        buttons[index].config(bg="#ffc8dd")
        if b1 == -1:
            b1 = index
            text1 = btn["text"]
        else:
            b2 = index
            text2 = btn["text"]
            buttons[b1].config(bg="#FF6F61")
            buttons[b2].config(bg="#FF6F61")
            if pary.get(text1) == text2:
                buttons[b1].config(bg="#bde0fe", state="disabled")
                buttons[b2].config(bg="#bde0fe", state="disabled")
                b1 = -1
            else:
                w.after(1000, lambda: reset_buttons(b1, b2))

    x = 0
    for i in range(4):
        for j in range(4):
            btn = Button(w2, text=slova[x], bg="lavender", width=25, height=5, font=("Helvetica", 10, "bold"), command=lambda b=x: pexeso(buttons[b], b))
            btn.grid(row=i, column=j, padx=5, pady=5)
            buttons.append(btn)
            x += 1
    reset = Button(w2, text="Reset", bg="#ffd6a5", font=("Helvetica", 10, "bold"), width=16, height=2, command=lambda: main_pexeso(soubor, 0))
    reset.grid(row=5, column=0, columnspan=2)
    hotovo = Button(w2, text="Hotovo", bg="#ffd6a5", font=("Helvetica", 10, "bold"), width=16, height=2, command=lambda: w2.destroy())
    hotovo.grid(row=5, column=2, columnspan=2)
def zpet(btn, zpet):
    for i in btn:
        i.grid_forget()
    zpet.grid_forget()
    play_btn.grid(row=0, column=0, pady=20, padx=280)
    create_btn.grid(row=1, column=0, pady=20, padx=280)
    login_btn.grid(row=2, column=0, pady=20, padx=280)
    sign_up_btn.grid(row=3, column=0, pady=20, padx=280)
    exit_btn.place(x=670, y=325)
    help_btn.place(x=15, y=325)
    log_btn.place(x=670, y=15)
def play():
    # Smazání startovacích tlačítek
    play_btn.grid_forget()
    create_btn.grid_forget()
    login_btn.grid_forget()
    sign_up_btn.grid_forget()
    exit_btn.place_forget()
    help_btn.place_forget()
    log_btn.place_forget()


    w.grid_columnconfigure(0, weight=1)
    w.grid_columnconfigure(3, weight=1)

    cursor.execute('SELECT * FROM sys.tables;')
    txt_s = cursor.fetchall()
    txt_s = txt_s[1:]
    txt_s = [table[0] for table in txt_s if table[0].startswith("p_")]

    button = []
    for idx, txt in enumerate(txt_s):
        btn = Button(w, text=txt[2:], bg="#a0c4ff", width=30, height=3, command=lambda t=txt: main_pexeso(t, 1))
        btn.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)
        button.append(btn)

    zpet_play = Button(w, text="Zpět", bg="#ffafcc", font=font, command=lambda : zpet(button, zpet_play))
    zpet_play.grid(row=len(txt_s) // 2 + 1, column=1, pady=20)
def vytvoření(pex, name, name_entry, btn, zpet):
    p = [k.get() for k in pex]
    cursor.execute(f'CREATE TABLE {name.get()}(value TEXT);')
    cursor.execute(f'INSERT INTO main(name) VALUES (?);', (name.get()))
    for i in p:
        cursor.execute(f'INSERT INTO {name.get()}(value) VALUES (?);', (i,))

    hotovo = messagebox.showinfo("Vytvořeno", "Pexeso bylo úspěšně vytvořeno.\nMůžete si ho nyní zahrát v Play!")

    conn.commit()

    zpet1(pex, name, name_entry, btn, zpet)
def zpet1(entries, name_entry, name_l, start_btn, zpet_btn):
    for i in entries:
        i.grid_forget()
    zpet_btn.grid_forget()
    name_entry.grid_forget()
    name_l.grid_forget()
    start_btn.grid_forget()
    play_btn.grid(row=0, column=0, pady=20, padx=280)
    create_btn.grid(row=1, column=0, pady=20, padx=280)
    login_btn.grid(row=2, column=0, pady=20, padx=280)
    sign_up_btn.grid(row=3, column=0, pady=20, padx=280)
    exit_btn.place(x=670, y=325)
    help_btn.place(x=15, y=325)
    log_btn.place(x=670, y=15)
def create():
    play_btn.grid_forget()
    create_btn.grid_forget()
    login_btn.grid_forget()
    sign_up_btn.grid_forget()
    exit_btn.place_forget()
    help_btn.place_forget()
    log_btn.place_forget()

    w.grid_columnconfigure(0, weight=1)
    w.grid_columnconfigure(3, weight=1)

    name_l = Label(w, text="Název:", bg="#f7f3e9", font=("Helvetica", 12))
    name_l.grid(row=0, column=0, pady=10)
    name_entry = Entry(w, font=("Helvetica", 12))
    name_entry.grid(row=0, column=1, pady=10)

    entries = []
    for i in range(8):
        for j in range(2):
            entry = Entry(w, width=15, font=("Helvetica", 10))
            entry.grid(row=i + 1, column=j, padx=5, pady=5)
            entries.append(entry)

    start_btn = Button(w, text="Start", bg="#ffafcc", font=font, width=15, command=lambda: vytvoření(entries, name_entry, name_l, start_btn, zpet_btn))
    start_btn.grid(row=9, column=1, pady=10)
    zpet_btn = Button(w, text="Zpět", bg="#ffafcc", font=font, width=15, command=lambda: zpet1(entries, name_entry, name_l, start_btn, zpet_btn))
    zpet_btn.grid(row=9, column=0, pady=10)
def zpet2(entry, label, remember, remember_ra, start_btn, zpet_btn, oko, oko_1, l, l1):
    for i in entry:
        i.grid_forget()
    for i in label:
        i.grid_forget()

    entry[1].unbind('<KeyRelease>')
    entry[2].unbind('<KeyRelease>')
    entry[3].unbind('<KeyRelease>')

    forget_g = [remember, remember_ra, start_btn, zpet_btn]
    forget_p = [oko, oko_1, l, l1]

    for g in forget_g:
        g.grid_forget()
    for p in forget_p:
        p.place_forget()
    play_btn.grid(row=0, column=0, pady=20, padx=280)
    create_btn.grid(row=1, column=0, pady=20, padx=280)
    login_btn.grid(row=2, column=0, pady=20, padx=280)
    sign_up_btn.grid(row=3, column=0, pady=20, padx=280)
    exit_btn.place(x=670, y=325)
    help_btn.place(x=15, y=325)
    log_btn.place(x=670, y=15)
def login_first(entry, label, remember, remember_ra, start_btn, zpet_btn, oko, oko_1, var, l, l1):
    global name
    if agree == False:
        error = messagebox.showerror("Nelze přihlásit", "Nickname nelze použít")
    elif entry[2].get() != entry[3].get():
        error = messagebox.showerror("Nelze přihlásit", "Hesla se neshodují")
    elif entry[0].get() == "" or entry[1].get() == "" or entry[2].get() == "" or entry[3].get() == "":
        error = messagebox.showerror("Nelze přihlásit", "Prázdné pole")
    else:
        cursor.execute('INSERT INTO login(name, password, email) VALUES (?, ?, ?);',
               (entry[1].get(), entry[2].get(), entry[0].get()))
        cursor.commit()
        name = entry[1].get()
        log_btn.config(text=name)
        if var.get() == 1:
            with open("login.txt", "w", encoding='utf-8') as file:
                file.write(f"{entry[1].get()}\n{entry[2].get()}")
        zpet2(entry, label, remember, remember_ra, start_btn, zpet_btn, oko, oko_1, l, l1)
def sign_up():
    play_btn.grid_forget()
    create_btn.grid_forget()
    login_btn.grid_forget()
    sign_up_btn.grid_forget()
    log_btn.place_forget()

    w.grid_columnconfigure(0, weight=1)
    w.grid_columnconfigure(3, weight=1)

    cursor.execute(f'SELECT name FROM login;')
    nickname = cursor.fetchall()

    def oko1(entry, oko):
        if entry.cget('show') == '*':
            entry.config(show="")
            oko.config(bg="grey")
        else:
            entry.config(show='*')
            oko.config(bg="white")

    def rovnost(event, entry, l):
        if entry[2].get() == entry[3].get():
            l.config(text="Hesla se shodují!", fg="green")
            l.place(x=390, y=170)
        elif entry[2].get() != entry[3].get():
            l.config(text="Hesla se neshodují!", fg="red")
            l.place(x=390, y=170)

    def nick(event, entry, l):
        global agree
        for x in nickname:
            if x[0] == entry[1].get():
                l.config(text="nickname už je použitý!", fg="red")
                l.place(x=390, y=78)
                agree = False
                break
            else:
                agree = True
                l.place_forget()

    name = ["e-mail:", "nickname:", "password:", "confrim password:"]
    entry = []
    label = []
    for x in range(4):
        l = Label(w, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
        l.grid(row=x, column=0, pady=10)
        label.append(l)
        if name[x] == "password:" or name[x] == "confrim password:":
            e = Entry(w, font=("Helvetica", 12), show="*")
        else:
            e = Entry(w, font=("Helvetica", 12))
        e.grid(row=x, column=1, pady=10)
        entry.append(e)

    image = Image.open("eye-icon-vector-illustration.jpg")
    image = image.resize((10, 10), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    oko = Button(w, image=photo, command=lambda: oko1(entry[2], oko))
    oko.photo = photo
    oko.place(x=586, y=104)

    oko_1 = Button(w, image=photo, command=lambda: oko1(entry[3], oko_1))
    oko_1.photo = photo
    oko_1.place(x=586, y=149)

    var = IntVar()

    remember = Label(w, text="remember me", bg="#f7f3e9", font=("Helvetica", 12, "bold"))
    remember.grid(row=4, column=0, pady=15)
    remember_ra = Checkbutton(w, font=("Helvetica", 12), variable=var, onvalue=1)
    remember_ra.grid(row=4, column=1, pady=15)

    l = Label(w)
    l1 = Label(w)

    start_btn = Button(w, text="Login", bg="#ffafcc", font=("Helvetica", 12, "bold"), width=15,
                       command=lambda: login_first(entry, label, remember, remember_ra, start_btn, zpet_btn, oko, oko_1,
                                                   var, l, l1))
    start_btn.grid(row=5, column=1, pady=10)
    zpet_btn = Button(w, text="Zpět", bg="#ffafcc", font=("Helvetica", 12, "bold"), width=15,
                      command=lambda: zpet2(entry, label, remember, remember_ra, start_btn, zpet_btn, oko, oko_1, l,
                                            l1))
    zpet_btn.grid(row=5, column=0, pady=10)

    entry[2].bind('<KeyRelease>', lambda event: rovnost(event, entry, l))
    entry[3].bind('<KeyRelease>', lambda event: rovnost(event, entry, l))
    entry[1].bind('<KeyRelease>', lambda event: nick(event, entry, l1))
def zpet3(frame, oko, remember, remember_ra):
    frame.place_forget()
    oko.place_forget()
    remember.grid_forget()
    remember_ra.grid_forget()
    play_btn.grid(row=0, column=0, pady=20, padx=280)
    create_btn.grid(row=1, column=0, pady=20, padx=280)
    login_btn.grid(row=2, column=0, pady=20, padx=280)
    sign_up_btn.grid(row=3, column=0, pady=20, padx=280)
    exit_btn.place(x=670, y=325)
    help_btn.place(x=15, y=325)
    log_btn.place(x=670, y=15)
def login_second(entry, frame, oko, remember, remember_ra, var):
    global name
    cursor.execute(f'SELECT password FROM login WHERE name LIKE ?;', (entry[0].get(),))
    password_right = cursor.fetchall()
    print(password_right)
    if password_right == []:
        error = messagebox.showerror("Nelze přihlásit", "Nickname neexistuje!")
    elif password_right[0][0] != entry[1].get():
        error = messagebox.showerror("Nelze přihlásit", "Nesprávné heslo!")
    else:
        name = entry[0].get()
        log_btn.config(text=name)
        if var.get() == 1:
            with open("login.txt", "w", encoding='utf-8') as file:
                file.write(f"{entry[0].get()}\n{entry[1].get()}")
        zpet3(frame, oko, remember, remember_ra)
def login():
    play_btn.grid_forget()
    create_btn.grid_forget()
    login_btn.grid_forget()
    sign_up_btn.grid_forget()
    exit_btn.place_forget()
    help_btn.place_forget()
    log_btn.place_forget()

    w.grid_rowconfigure(0, weight=1)  # Vyvážení prostoru nad rámečkem
    w.grid_rowconfigure(1, weight=1)  # Vyvážení prostoru pod rámečkem
    w.grid_columnconfigure(0, weight=1)  # Vyvážení prostoru vlevo od rámečku
    w.grid_columnconfigure(1, weight=1)

    def oko1(entry, oko):
        if entry.cget('show') == '*':
            entry.config(show="")
            oko.config(bg="grey")
        else:
            entry.config(show='*')
            oko.config(bg="white")

    name = ["nickname:", "password:"]
    entry = []
    label = []
    frame = Frame(w, bg='lightblue', width=600, height=400, highlightbackground="#ffd6a5", highlightthickness=4)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    for x in range(2):
        l = Label(frame, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
        l.grid(row=x, column=0, pady=20, padx=20, sticky='nsew')
        label.append(l)
        if name[x] == "password:":
            e = Entry(frame, font=("Helvetica", 12), show="*")
        else:
            e = Entry(frame, font=("Helvetica", 12))
        e.grid(row=x, column=1, pady=20, padx=30, sticky='nsew')
        entry.append(e)

    image = Image.open("eye-icon-vector-illustration.jpg")
    image = image.resize((10, 10), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    oko = Button(w, image=photo, command=lambda: oko1(entry[1], oko))
    oko.photo = photo
    oko.place(x=560, y=170)

    var = IntVar()

    remember = Label(frame, text="remember me:", bg="#f7f3e9", font=("Helvetica", 12, "bold"))
    remember.grid(row=2, column=0, pady=15)
    remember_ra = Checkbutton(frame, font=("Helvetica", 12), variable=var, onvalue=1)
    remember_ra.grid(row=2, column=1)

    start_btn = Button(frame, text="Login", bg="#ffafcc", font=font, width=5, command=lambda: login_second(entry, frame, oko, remember, remember_ra, var))
    start_btn.grid(row=3, column=1)
    zpet_btn = Button(frame, text="Zpět", bg="#ffafcc", font=font, width=5, command=lambda: zpet3(frame, oko, remember, remember_ra))
    zpet_btn.grid(row=3, column=0, pady=10)

play_btn = Button(w, text="Play", bg="#a0c4ff", width=20, height=2, font=font, command=play)
play_btn.grid(row=0, column=0, pady=20, padx=290)
create_btn = Button(w, text="Create", bg="#a0c4ff", width=20, height=2, font=font, command=create)
create_btn.grid(row=1, column=0, pady=20, padx=290)
login_btn = Button(w, text="Login", bg="#a0c4ff", width=20, height=2, font=font, command=login)
login_btn.grid(row=2, column=0, pady=20, padx=290)
sign_up_btn = Button(w, text="Sign up", bg="#a0c4ff", width=20, height=2, font=font, command=sign_up)
sign_up_btn.grid(row=3, column=0, pady=20, padx=290)
exit_btn = Button(w, text="Quit", bg="#a0c4ff", width=10, height=2, font=font, command=lambda: w.quit())
exit_btn.place(x=670, y=325)
help_btn = Button(w, text="Help", bg="#a0c4ff", width=10, height=2, font=font, command=lambda: w.quit())
help_btn.place(x=15, y=325)
log_btn = Button(w, text=name, bg="#ffafcc", font=font, command=lambda: w.quit())
log_btn.place(x=700, y=15)

try:
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=KRAZAZI\SQLEXPRESS;'
        'DATABASE=Pexeso;'
        'UID=krazazi;'
        'PWD=Pernicek@2024;'
    )
    cursor = conn.cursor()
    w.mainloop()
except Exception as e:
    messagebox.showerror("SQL connecting Error", e)