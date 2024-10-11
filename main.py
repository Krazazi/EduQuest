import bcrypt
from tkinter import *
from tkinter import messagebox
import random
import pyodbc
from PIL import Image, ImageTk

w = Tk()
w.title("EduQuest")
w.configure(bg="#f7f3e9")  # Jemná pastelová barva pozadí
w.geometry("800x400")
w.iconbitmap("OIP.ico")
w.resizable(False, False)

font = ("Helvetica", 12, "bold")

w2 = None
hide = BooleanVar(value=True)
name = None
agree = None
databaze = None

with open("login.txt", "r") as login:
    name = login.readline().strip()
    if name == "":
        name = "Login"

with open("h.txt", "r") as h:
    h = int(h.readline().strip())
    if h == 0:
        hide.set(False)
    else:
        hide.set(True)

class Objekty:
    def __init__(self, druh, **kwargs):
        self.druh = druh
        self.widgets = {
            "Button": Button,
            "Label": Label,
            "Entry": Entry,
            "Radiobutton": Radiobutton,
            "Checkbutton": Checkbutton,
            "Frame": Frame,
            "Listbox": Listbox
        }
        if self.druh in self.widgets:
            self.widget = self.widgets[self.druh](**kwargs)

    def grid(self, **kwargs):
        self.widget.grid(**kwargs)
    def grid_forget(self):
        self.widget.grid_forget()
    def place(self, **kwargs):
        self.widget.place(**kwargs)
    def place_forget(self):
        self.widget.place_forget()
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
    def pack_forget(self):
        self.widget.pack_forget()
    def config(self, **kwargs):
        self.widget.config(**kwargs)
    def bind(self, event, handler):
        self.widget.bind(event, handler)
    def unbind(self, key):
        self.widget.unbind(key)
    def insert(self, index, text):
        self.widget.insert(index, text)
    def get(self):
        self.widget.get()
    def set(self, value):
        self.widget.set(value)
    def cget(self, typ):
        self.widget.cget(typ)
    def grid_columnconfigure(self, num, **kwargs):
        self.widget.grid_columnconfigure(num, **kwargs)
    def pack_columnconfigure(self, num, **kwargs):
        self.widget.pack_columnconfigure(num, **kwargs)

def hide_main(num):
    play_btn.grid_forget()
    create_btn.grid_forget()
    login_btn.grid_forget()
    sign_up_btn.grid_forget()
    log_btn.place_forget()
    if num == 1:
        exit_btn.place_forget()
        help_btn.place_forget()
def show_main(frame, bind):
    frame.pack_forget()
    if not bind == []:
        bind[1].unbind('<KeyRelease>')
        bind[2].unbind('<KeyRelease>')
        bind[3].unbind('<KeyRelease>')
    play_btn.grid(row=0, column=0, pady=20, padx=280)
    create_btn.grid(row=1, column=0, pady=20, padx=280)
    login_btn.grid(row=2, column=0, pady=20, padx=280)
    sign_up_btn.grid(row=3, column=0, pady=20, padx=280)
    exit_btn.place(x=670, y=325)
    help_btn.place(x=15, y=325)
    log_btn.place(x=670, y=15)
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
        w2.iconbitmap("OIP.ico")

    slova = list(pary.keys())
    random.shuffle(slova)

    buttons = []
    b1 = -1
    text1 = None

    def reset_buttons(b, b2):
        nonlocal b1
        buttons[b].config(bg="lavender")
        buttons[b2].config(bg="lavender")
        if hide.get():
            buttons[b].config(text="   ")
            buttons[b2].config(text="   ")
        b1 = -1

    def pexeso(btn, index):
        nonlocal b1, text1
        buttons[index].config(bg="#ffc8dd")
        if b1 == -1:
            b1 = index
            text1 = slova[index]
            btn.config(text=slova[index])
        else:
            b2 = index
            text2 = slova[index]
            buttons[b1].config(bg="#FF6F61")
            buttons[b2].config(bg="#FF6F61")
            btn.config(text=slova[index])
            if pary.get(text1) == text2:
                buttons[b1].config(bg="#bde0fe", state="disabled")
                buttons[b2].config(bg="#bde0fe", state="disabled")
                b1 = -1
            else:
                w.after(1000, lambda: reset_buttons(b1, b2))

    x = 0
    for i in range(4):
        for j in range(4):
            btn = Objekty("Button", master=w2, text=slova[x], bg="lavender", width=25, height=5, font=("Helvetica", 10, "bold"), command=lambda b=x: pexeso(buttons[b], b))
            btn.grid(row=i, column=j, padx=5, pady=5)
            if hide.get():
                btn.config(text="    ")
            buttons.append(btn)
            x += 1
    reset = Objekty("Button", master=w2, text="Reset", bg="#ffd6a5", font=("Helvetica", 10, "bold"), width=16, height=2, command=lambda: main_pexeso(soubor, 0))
    reset.grid(row=5, column=0, columnspan=2)
    hotovo = Objekty("Button", master=w2, text="Hotovo", bg="#ffd6a5", font=("Helvetica", 10, "bold"), width=16, height=2, command=lambda: w2.destroy())
    hotovo.grid(row=5, column=2, columnspan=2)
def play():
    if not databaze:
        messagebox.showerror("SQL connecting Error", "Nejste připojen k Databázi!")
    else:
        hide_main(1)

        w.grid_columnconfigure(0, weight=0)
        w.grid_columnconfigure(3, weight=0)
        w.grid_rowconfigure(0, weight=0)
        w.grid_rowconfigure(1, weight=0)

        cursor.execute('SELECT * FROM sys.tables;')
        txt_s = cursor.fetchall()
        txt_s = [table[0] for table in txt_s if table[0].startswith("p_")]

        button = []
        frame = Objekty("Frame", master=w, bg="#f7f3e9")
        frame.pack()
        for idx, txt in enumerate(txt_s):
            btn = Objekty("Button", master=frame.widget, text=txt[2:], bg="#a0c4ff", width=30, height=3, command=lambda t=txt: main_pexeso(t, 1))
            btn.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)
            button.append(btn)

        zpet_play = Objekty("Button", master=frame.widget, text="Zpět", bg="#ffafcc", font=font, command=lambda: show_main(frame, []))
        zpet_play.grid(row=len(txt_s) // 2 + 1, column=1, pady=20)
def create():
    if not databaze:
        messagebox.showerror("SQL connecting Error", "Nejste připojen k Databázi!")
    elif name == "Login":
        login()
    else:
        hide_main(1)

        w.grid_columnconfigure(0, weight=1)
        w.grid_columnconfigure(3, weight=1)
        w.grid_rowconfigure(0, weight=0)
        w.grid_rowconfigure(1, weight=0)

        def vytvoření(pex, namex, name_entry, btn, zpet):
            p = [k.get() for k in pex]
            n = namex.get().replace('-', '_')
            cursor.execute(f'CREATE TABLE p_{n}(value TEXT);')
            cursor.execute(f'INSERT INTO main(name) VALUES (?);', (n))
            cursor.execute(f"SELECT pexes_v FROM login WHERE name LIKE ?", (name,))
            cursor.execute('UPDATE login SET pexes_v = ? WHERE name = ?', (cursor.fetchone()[0] + 1, name))
            for i in p:
                cursor.execute(f'INSERT INTO p_{n}(value) VALUES (?);', (i,))

            hotovo = messagebox.showinfo("Vytvořeno",
                                         "Pexeso bylo úspěšně vytvořeno.\nMůžete si ho nyní zahrát v Play!")

            conn.commit()

            zpet(pex, namex, name_entry, btn, zpet)

        def zpet(entries, name_entry, name_l, start_btn, zpet_btn):
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

        name_l = Objekty("Label", master=w, text="Název:", bg="#f7f3e9", font=("Helvetica", 12))
        name_l.grid(row=0, column=0, pady=10)
        name_entry = Objekty("Entry", master=w, font=("Helvetica", 12))
        name_entry.grid(row=0, column=1, pady=10)

        entries = []
        for i in range(8):
            for j in range(2):
                entry = Objekty("Entry", master=w, width=15, font=("Helvetica", 10))
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                entries.append(entry)

        start_btn = Objekty("Button", master=w, text="Vytvořit", bg="#ffafcc", font=font, width=15,
                           command=lambda: vytvoření(entries, name_entry, name_l, start_btn, zpet_btn))
        start_btn.grid(row=9, column=1, pady=10)
        zpet_btn = Objekty("Button", master=w, text="Zpět", bg="#ffafcc", font=font, width=15,
                          command=lambda: zpet(entries, name_entry, name_l, start_btn, zpet_btn))
        zpet_btn.grid(row=9, column=0, pady=10)
def sign_up():
    if not databaze:
        messagebox.showerror("SQL connecting Error", "Nejste připojen k Databázi!")
    else:
        hide_main(0)

        w.grid_rowconfigure(0, weight=0)
        w.grid_rowconfigure(1, weight=0)
        w.grid_columnconfigure(0, weight=1)
        w.grid_columnconfigure(3, weight=1)

        cursor.execute(f'SELECT name FROM login;')
        nickname = cursor.fetchall()

        def login_first(entry, var, frame):
            global name
            if agree == False:
                error = messagebox.showerror("Nelze přihlásit", "Nickname nelze použít")
            elif entry[2].widget.get() != entry[3].widget.get():
                error = messagebox.showerror("Nelze přihlásit", "Hesla se neshodují")
            elif entry[0].widget.get() == "" or entry[1].widget.get() == "" or entry[2].widget.get() == "" or entry[3].widget.get() == "":
                error = messagebox.showerror("Nelze přihlásit", "Prázdné pole")
            else:
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(entry[2].widget.get().encode('utf-8'), salt)
                password = hashed.decode('utf-8')
                cursor.execute('INSERT INTO login(name, password, email, pexeso, pexes_v) VALUES (?, ?, ?, ?, ?);',
                               (entry[1].widget.get(), password, entry[0].widget.get(), 0, 0))
                cursor.commit()
                name = entry[1].widget.get()
                log_btn.config(text=name)
                if var.get() == 1:
                    with open("login.txt", "w", encoding='utf-8') as file:
                        file.write(f"{entry[1].widget.get()}\n{entry[2].widget.get()}")
                show_main(frame, entry)

        def oko1(entry, oko):
            if entry.widget.cget("show") == "*":
                entry.config(show="")
                oko.config(bg="grey")
            else:
                entry.config(show='*')
                oko.config(bg="white")

        def rovnost(event, entry, l):
            if entry[2].widget.get() == entry[3].widget.get():
                l.config(text="Hesla se shodují!", fg="green")
            else:
                l.config(text="Hesla se neshodují!", fg="red")
            l.place(x=210, y=170)

        def nick(event, entry, l):
            global agree
            for x in nickname:
                if x[0] == entry[1].widget.get():
                    l.config(text="nickname už je použitý!", fg="red")
                    l.place(x=210, y=78)
                    agree = False
                    break
                else:
                    agree = True
                    l.place_forget()

        name = ["e-mail:", "nickname:", "password:", "confrim password:"]
        entry = []
        label = []
        frame = Objekty("Frame", master=w, width=600, height=400, bg='lightblue', highlightbackground="#ffd6a5", highlightthickness=4)
        frame.pack(ipady=20, ipadx=50)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        for x in range(4):
            l = Objekty("Label", master=frame.widget, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
            l.grid(row=x, column=0, pady=10)
            label.append(l)
            if name[x] == "password:" or name[x] == "confrim password:":
                e = Objekty("Entry", master=frame.widget, font=("Helvetica", 12), show="*")
            else:
                e = Objekty("Entry", master=frame.widget, font=("Helvetica", 12))
            e.grid(row=x, column=1, pady=10)
            entry.append(e)

        image = Image.open("eye-icon-vector-illustration.jpg")
        image = image.resize((10, 10), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        oko = Objekty("Button", master=frame.widget, image=photo, command=lambda: oko1(entry[2], oko))
        oko.photo = photo
        oko.place(x=400, y=104)

        oko_1 = Objekty("Button", master=frame.widget, image=photo, command=lambda: oko1(entry[3], oko_1))
        oko_1.photo = photo
        oko_1.place(x=400, y=150)

        var = IntVar()

        remember = Objekty("Label", master=frame.widget, text="remember me", bg="#f7f3e9", font=("Helvetica", 12, "bold"))
        remember.grid(row=4, column=0, pady=15)
        remember_ra = Objekty("Checkbutton", master=frame.widget, font=("Helvetica", 12), variable=var, onvalue=1)
        remember_ra.grid(row=4, column=1, pady=15)

        l = Objekty("Label", master=frame.widget)
        l1 = Objekty("Label", master=frame.widget)

        start_btn = Objekty("Button", master=frame.widget, text="Login", bg="#ffafcc", font=("Helvetica", 12, "bold"), width=15,
                           command=lambda: login_first(entry, var, frame))
        start_btn.grid(row=5, column=1, pady=10)
        zpet_btn = Objekty("Button", master=frame.widget, text="Zpět", bg="#ffafcc", font=("Helvetica", 12, "bold"), width=15,
                          command=lambda: show_main(frame, entry))
        zpet_btn.grid(row=5, column=0, pady=10)

        entry[2].bind('<KeyRelease>', lambda event: rovnost(event, entry, l))
        entry[3].bind('<KeyRelease>', lambda event: rovnost(event, entry, l))
        entry[1].bind('<KeyRelease>', lambda event: nick(event, entry, l1))
def login():
    if not databaze:
        messagebox.showerror("SQL connecting Error", "Nejste připojen k Databázi!")
    else:
        hide_main(0)

        w.grid_rowconfigure(0, weight=1)
        w.grid_rowconfigure(1, weight=1)
        w.grid_columnconfigure(0, weight=1)
        w.grid_columnconfigure(1, weight=1)

        def login_second(entry, frame, var):
            global name
            cursor.execute("SELECT password FROM login WHERE name = ?", (entry[0].widget.get(),))
            result = cursor.fetchone()
            if not result:
                error = messagebox.showerror("Nelze přihlásit", "Nickname neexistuje!")
            else:
                hashed_password = result[0].encode('utf-8')
                heslo = bcrypt.checkpw(entry[1].widget.get().encode('utf-8'), hashed_password)
                if heslo:
                    name = entry[0].widget.get()
                    log_btn.config(text=name)
                    if var.get() == 1:
                        with open("login.txt", "w", encoding='utf-8') as file:
                            file.write(f"{entry[0].widget.get()}\n{entry[1].widget.get()}")
                    show_main(frame, [])
                else:
                    error = messagebox.showerror("Nelze přihlásit", "Nesprávné heslo!")

        def oko1(entry, oko):
            if entry.widget.cget("show") == "*":
                entry.config(show="")
                oko.config(bg="grey")
            else:
                entry.config(show='*')
                oko.config(bg="white")

        name = ["nickname:", "password:"]
        entry = []
        label = []
        frame = Objekty("Frame", master=w, bg='lightblue', width=600, height=400, highlightbackground="#ffd6a5", highlightthickness=4)
        frame.pack(pady=50)
        for x in range(2):
            l = Objekty("Label", master=frame.widget, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
            l.grid(row=x, column=0, pady=20, padx=20, sticky='nsew')
            label.append(l)
            if name[x] == "password:":
                e = Objekty("Entry", master=frame.widget, font=("Helvetica", 12), show="*")
            else:
                e = Objekty("Entry", master=frame.widget, font=("Helvetica", 12))
            e.grid(row=x, column=1, pady=20, padx=30, sticky='nsew')
            entry.append(e)

        image = Image.open("eye-icon-vector-illustration.jpg")
        image = image.resize((10, 10), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        oko = Objekty("Button", master=frame.widget, image=photo, command=lambda: oko1(entry[1], oko))
        oko.photo = photo
        oko.place(x=345, y=90)

        var = IntVar()

        remember = Objekty("Label", master=frame.widget, text="remember me:", bg="#f7f3e9", font=("Helvetica", 12, "bold"))
        remember.grid(row=2, column=0, pady=15)
        remember_ra = Objekty("Checkbutton", master=frame.widget, font=("Helvetica", 12), variable=var, onvalue=1)
        remember_ra.grid(row=2, column=1)

        start_btn = Objekty("Button", master=frame.widget, text="Login", bg="#ffafcc", font=font, width=5,
                           command=lambda: login_second(entry, frame, var))
        start_btn.grid(row=3, column=1)
        zpet_btn = Objekty("Button", master=frame.widget, text="Zpět", bg="#ffafcc", font=font, width=5,
                          command=lambda: show_main(frame, []))
        zpet_btn.grid(row=3, column=0, pady=10)
def user():
    global name
    if not databaze:
        messagebox.showerror("SQL connecting Error", "Nejste připojen k Databázi!")
    elif name == "Login":
        login()
    else:
        hide_main(0)

        w.grid_rowconfigure(0, weight=1)
        w.grid_rowconfigure(1, weight=1)
        w.grid_columnconfigure(0, weight=1)
        w.grid_columnconfigure(1, weight=1)

        def on_enter(event):
            event.widget.config(fg="blue")

        def on_leave(event):
            event.widget.config(fg="black")

        def on_click(event):
            print("Label byl kliknut!")

        def hide_p():
            if hide.get():
                h = 1
            elif not hide.get():
                h = 0

            with open("h.txt", "w") as h_txt:
                h_txt.write(str(h))

        frame = Objekty("Frame", master=w, bg='lightblue', width=600, height=400, highlightbackground="#ffd6a5", highlightthickness=4)
        frame.pack(pady=50)

        l = Objekty("Entry", master=frame.widget, bg="#f7f3e9", font=font)
        l.grid(row=0, column=1, columnspan=2, pady=10, padx=50)
        l.insert(0, name)

        words = ["pexeso", "pexes_v"]
        proslov = ["Splněných Pexes: ", "Vytvořených Pexes: "]
        for s in range(len(words)):
            cursor.execute(f"SELECT {words[s]} FROM login WHERE name LIKE ?", (name,))
            pexeso = cursor.fetchone()
            pex = Objekty("Label", master=frame.widget, text=proslov[s]+str(pexeso[0]), bg="#f7f3e9", font=font)
            pex.grid(row=s+1, column=1, columnspan=2, pady=10, padx=50)
            pex.bind("<Enter>", on_enter)
            pex.bind("<Leave>", on_leave)
            pex.bind("<Button-1>", on_click)

        hide_pex = Objekty("Checkbutton", master=frame.widget, text="Pexeso hide", variable=hide, font=font, onvalue=True, command=hide_p)
        hide_pex.grid(row=len(words) + 1, column=1, pady=10, padx=50)

        label = Objekty("Label", master=frame.widget, text="Změnit heslo", fg="black", font=font)
        label.grid(row=len(words)+1, column=2, pady=10, padx=50)

        zpet_btn = Objekty("Button", master=frame.widget, text="Zpět", bg="#ffafcc", font=font, width=5, command=lambda: show_main(frame, []))
        zpet_btn.grid(row=len(words)+2, column=1, pady=10, padx=10)
        uloz_btn = Objekty("Button", master=frame.widget, text="Uložit", bg="#ffafcc", font=font, width=5, command=lambda: show_main(frame, []))
        uloz_btn.grid(row=len(words) + 2, column=2, pady=10, padx=10)

        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.bind("<Button-1>", on_click)
def admin():
    if name == "admin":
        w.unbind(f"<KeyPress-{key}>")
        w.unbind(f"<KeyRelease-{key}>")

        admin_w = Toplevel()
keys = {
    'a': False,
    'd': False,
    'm': False,
    'i': False,
    'n': False
}
def update_key_state(event, state):
    keys[event.keysym] = state
    if all(keys.values()):
        admin()
for key in keys.keys():
    w.bind(f"<KeyPress-{key}>", lambda event: update_key_state(event, True))
    w.bind(f"<KeyRelease-{key}>", lambda event: update_key_state(event, False))

play_btn = Objekty("Button", master=w, text="Play", bg="#a0c4ff", width=20, height=2, font=font, command=play)
play_btn.grid(row=0, column=0, pady=20, padx=290)
create_btn = Objekty("Button", master=w, text="Create", bg="#a0c4ff", width=20, height=2, font=font, command=create)
create_btn.grid(row=1, column=0, pady=20, padx=290)
login_btn = Objekty("Button", master=w, text="Login", bg="#a0c4ff", width=20, height=2, font=font, command=login)
login_btn.grid(row=2, column=0, pady=20, padx=290)
sign_up_btn = Objekty("Button", master=w, text="Sign up", bg="#a0c4ff", width=20, height=2, font=font, command=sign_up)
sign_up_btn.grid(row=3, column=0, pady=20, padx=290)
exit_btn = Objekty("Button", master=w, text="Quit", bg="#a0c4ff", width=10, height=2, font=font, command=lambda: w.quit())
exit_btn.place(x=670, y=325)
help_btn = Objekty("Button", master=w, text="Help", bg="#a0c4ff", width=10, height=2, font=font, command=lambda: w.quit())
help_btn.place(x=15, y=325)
log_btn = Objekty("Button", master=w, text=name, bg="#ffafcc", font=font, command=user)
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
    databaze = True
except Exception:
    databaze = False

w.mainloop()
