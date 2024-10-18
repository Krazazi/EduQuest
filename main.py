import bcrypt
from tkinter import *
from tkinter import messagebox
import random
import pyodbc
import time
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

image = Image.open("eye-icon-vector-illustration.jpg")
image = image.resize((10, 10), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

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
def create_hash(entry):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(entry.widget.get().encode('utf-8'), salt)
    password = hashed.decode('utf-8')
    return password
def unhash_password(entry, result):
    hashed_password = result[0].encode('utf-8')
    heslo = bcrypt.checkpw(entry[1].widget.get().encode('utf-8'), hashed_password)
    return heslo
def oko1(entry, oko):
        if entry.widget.cget("show") == "*":
            entry.config(show="")
            oko.config(bg="grey")
        else:
            entry.config(show='*')
            oko.config(bg="white")
def rovnost(event, entry, l):
        global agree
        if entry[0].widget.get() == entry[1].widget.get():
            l.config(text="Hesla se shodují!", fg="green")
            agree = True

        else:
            l.config(text="Hesla se neshodují!", fg="red")
            agree = False
        l.place(x=240, y=113)
def on_enter(event):
    event.widget.config(fg="blue")
def on_leave(event):
    event.widget.config(fg="black")
def new_password(frame, frame1):
    frame1.pack_forget()

    agree = False

    def change(entry):
        global name
        if entry[0].widget.get() != entry[1].widget.get():
            error = messagebox.showerror("Nelze přihlásit", "Hesla se neshodují")

        elif entry[0].widget.get() == "" or entry[1].widget.get() == "":
            error = messagebox.showerror("Nelze přihlásit", "Prázdné pole")
        else:
            password = create_hash(entry[0])
            cursor.execute(f"UPDATE login SET password = ? WHERE name = ?;", (password, name))
            cursor.commit()
            notification = messagebox.showinfo("Info", "Heslo bylo uspěšně změněno!")
            log_btn.config(text=name)

            show_main(frame1, [])

    def back():
        frame1.pack_forget()
        frame.pack(pady=50)

    name = ["new password:", "confrim password:"]
    entry = []
    frame1 = Objekty("Frame", master=w, bg='lightblue', width=600, height=400, highlightbackground="#ffd6a5",
                     highlightthickness=4)
    frame1.pack(pady=50)
    for x in range(2):
        l = Objekty("Label", master=frame1.widget, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
        l.grid(row=x, column=0, pady=20, padx=30, sticky='nsew')
        e = Objekty("Entry", master=frame1.widget, font=("Helvetica", 12), show="*")
        e.grid(row=x, column=1, pady=20, padx=30, sticky='nsew')
        entry.append(e)

    oko = Objekty("Button", master=frame1.widget, image=photo, command=lambda: oko1(entry[0], oko))
    oko.photo = photo
    oko.place(x=430, y=25)

    oko_1 = Objekty("Button", master=frame1.widget, image=photo, command=lambda: oko1(entry[1], oko_1))
    oko_1.photo = photo
    oko_1.place(x=430, y=90)

    l = Objekty("Label", master=frame1.widget)

    start_btn = Objekty("Button", master=frame1.widget, text="Potvrdit", bg="#ffafcc", font=font, width=5,
                        command=lambda: change(entry))
    start_btn.grid(row=4, column=1, ipadx=20, pady=10)
    zpet_btn = Objekty("Button", master=frame1.widget, text="Zpět", bg="#ffafcc", font=font, width=5,
                       command=back)
    zpet_btn.grid(row=4, column=0, ipadx=20, pady=10)

    entry[0].bind('<KeyRelease>', lambda event: rovnost(event, entry, l))
    entry[1].bind('<KeyRelease>', lambda event: rovnost(event, entry, l))
def e_mail(event, frame):
    global name
    try:
        code = random.randrange(111111, 999999)
        sender_email = "123krz@seznam.cz"
        sender_password = "**********"
        recipient_email = cursor.execute("select email from login where name like ?", (name, )).fetchall()[0][0]
        subject = "[EduQuest] Oveření vašeho zařízení"
        body = f""" Ahoj {name}!

        Pokus o změnu hesla vyžaduje další ověření, protože si nepamatujete vaše heslo. Chcete-li dokončit změnu hesla či přihlášení, zadejte ověřovací kód na nerozpoznaném zařízení.

        Ověřovací kód: {str(code)}

        Pokud jste se nepokusili přihlásit ke svému účtu, může být váš účet prozrazen. Navštivte naši aplikaci a vytvořte nové silné heslo pro svůj účet EduQuest.

        Díky,
        tým EduQuest"""

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.seznam.cz', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)

            frame.pack_forget()

            def back():
                frame1.pack_forget()
                frame.pack(pady=50)

            def control(entry, code):
                try:
                    if int(entry.widget.get()) == code:
                        new_password(frame, frame1)
                    else:
                        error = messagebox.showerror("Špratný kód", "Kód který jste zadali se neshoduje!")
                except:
                    error = messagebox.showerror("Špratný kód", "Kód který jste zadali se neshoduje!")

            frame1 = Objekty("Frame", master=w, bg='lightblue', width=600, height=400, highlightbackground="#ffd6a5",
                             highlightthickness=4)
            frame1.pack(pady=50)
            label1 = Objekty("Label", master=frame1.widget, text=f"Kód poslán na email:", fg="black", font=font)
            label1.grid(row=0, column=0, pady=10, padx=50)
            label2 = Objekty("Label", master=frame1.widget, text=recipient_email, fg="black", font=font)
            label2.grid(row=0, column=1, pady=10, padx=50)
            l = Objekty("Label", master=frame1.widget, text="Ověřovací kód:", bg="#f7f3e9",
                        font=("Helvetica", 12, "bold"))
            l.grid(row=1, column=0, pady=10, padx=20, sticky='nsew')
            e = Objekty("Entry", master=frame1.widget, font=("Helvetica", 12))
            e.grid(row=1, column=1, pady=10, padx=30, sticky='nsew')
            label = Objekty("Label", master=frame1.widget, text="Poslat znovu", fg="black", font=font)
            label.grid(row=2, column=1, pady=10, padx=50)

            start_btn = Objekty("Button", master=frame1.widget, text="Potvrdit", bg="#ffafcc", font=font, width=5,
                                command=lambda: control(e, code))
            start_btn.grid(row=3, column=1, ipadx=20, pady=10)
            zpet_btn = Objekty("Button", master=frame1.widget, text="Zpět", bg="#ffafcc", font=font, width=5,
                               command=back)
            zpet_btn.grid(row=3, column=0, ipadx=20, pady=10)

            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            label.bind("<Button-1>", lambda event: e_mail(event, frame1))

            server.quit()

        except Exception as e:
            error = messagebox.showerror("Chyba při odesílání e-mailu", f"Váš email neexistuje, napište na podporu")

    except:
        error = messagebox.showerror("Chyba při odesílání e-mailu", f"Váš nickname neexistuje!")
        frame.pack(pady=50)
        name = "Login"
def change_password(event, frame):
    frame.pack_forget()

    def change(entry, frame):
        global name
        cursor.execute("SELECT password FROM login WHERE name = ?", (entry[0].widget.get(),))
        result = cursor.fetchone()
        if not result:
            error = messagebox.showerror("Nelze přihlásit", "Nickname neexistuje!")
        else:
            heslo = unhash_password(entry, result)
            if heslo:
                password = create_hash(entry[2])
                cursor.execute(f"UPDATE login SET password = ? WHERE name = ?;", (password, entry[0].widget.get()))
                cursor.commit()

                show_main(frame1, [])
            else:
                error = messagebox.showerror("Chyba", "Nesprávné heslo!")
    def back():
        frame1.pack_forget()
        frame.pack(pady=50)

    def email(event, entry):
        global name
        name = entry[0].widget.get()
        e_mail(event, frame1)

    name = ["nickname:", "password:", "new password:"]
    entry = []
    label = []
    frame1 = Objekty("Frame", master=w, bg='lightblue', width=600, height=400, highlightbackground="#ffd6a5",
                    highlightthickness=4)
    frame1.pack(pady=50)
    for x in range(3):
        l = Objekty("Label", master=frame1.widget, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
        l.grid(row=x, column=0, pady=20, padx=20, sticky='nsew')
        label.append(l)
        if name[x] == "nickname:":
            e = Objekty("Entry", master=frame1.widget, font=("Helvetica", 12))
        else:
            e = Objekty("Entry", master=frame1.widget, font=("Helvetica", 12), show="*")
        e.grid(row=x, column=1, pady=20, padx=30, sticky='nsew')
        entry.append(e)

    oko = Objekty("Button", master=frame1.widget, image=photo, command=lambda: oko1(entry[1], oko))
    oko.photo = photo
    oko.place(x=380, y=90)

    oko1_button = Objekty("Button", master=frame1.widget, image=photo, command=lambda: oko1(entry[2], oko1_button))
    oko1_button.photo = photo
    oko1_button.place(x=380, y=155)

    label = Objekty("Label", master=frame1.widget, text="Zapomněl heslo", fg="black", font=font)
    label.grid(row=3, column=1, pady=10, padx=50)

    start_btn = Objekty("Button", master=frame1.widget, text="Login", bg="#ffafcc", font=font, width=5,
                        command=lambda: change(entry, frame1))
    start_btn.grid(row=4, column=1)
    zpet_btn = Objekty("Button", master=frame1.widget, text="Zpět", bg="#ffafcc", font=font, width=5,
                       command=back)
    zpet_btn.grid(row=4, column=0, pady=10)

    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)
    label.bind("<Button-1>", lambda event: email(event, entry))
def main_pexeso(soubor, num):
    global w2
    pary = {}
    cursor.execute(f'SELECT value FROM {soubor};')
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
    hotov = 0
    spatne = 0
    start_time = time.time()

    def reset_buttons(b, b2):
        nonlocal b1
        buttons[b].config(bg="lavender")
        buttons[b2].config(bg="lavender")
        if hide.get():
            buttons[b].config(text="   ")
            buttons[b2].config(text="   ")
        b1 = -1

    def pexeso(btn, index):
        nonlocal b1, text1, hotov, spatne, start_time
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
                hotov += 1
            else:
                w.after(1000, lambda: reset_buttons(b1, b2))
                spatne += 1
            if hotov == 8:
                end_time = time.time()
                elapsed_time = round(end_time - start_time, 2)
                if name != "Login":
                    cursor.execute(f'INSERT INTO {soubor}(username, time,  chyb) VALUES (?, ?, ?);', (name, elapsed_time, spatne))
                    cursor.commit()
                message = messagebox.showinfo("Hotovo", f"Pexeso splněno s {spatne} chybami za čas {elapsed_time}")

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

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def zpet(main, entry, zpet):
            main.pack_forget()
            entry.pack_forget()
            show_main(zpet, [])
        def filtr(event, button):
            if event.widget.get() == "":
                new_txt_s = txt_s
            else:
                new_txt_s = [table for table in txt_s if table.startswith(f"p_{event.widget.get()}")]

            for bt in button:
                bt.grid_forget()

            for idx, txt in enumerate(new_txt_s):
                btn = Objekty("Button", master=button_frame, text=txt[2:], bg="#a0c4ff", width=30, height=3,
                              command=lambda t=txt: main_pexeso(t, 1))
                btn.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)
                button.append(btn)

            button_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        cursor.execute('SELECT * FROM sys.tables;')
        txt_s = cursor.fetchall()
        txt_s = [table[0] for table in txt_s if table[0].startswith("p_")]

        button = []

        entry_frame = Frame(w)
        entry_frame.pack(side=TOP)  # Zajišťuje, že entry je nahoře
        input_e = Entry(entry_frame, font=("Italy", 20), width=53)
        input_e.pack(side=LEFT)

        main_frame = Frame(w, bg="#f7f3e9")
        main_frame.pack(fill=BOTH, expand=1)

        canvas = Canvas(main_frame, bg="#f7f3e9")
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        button_frame = Frame(canvas, bg="#f7f3e9")
        canvas.create_window((0, 0), window=button_frame, anchor="nw")

        for idx, txt in enumerate(txt_s):
            btn = Objekty("Button", master=button_frame, text=txt[2:], bg="#a0c4ff", width=30, height=3,
                          command=lambda t=txt: main_pexeso(t, 1))
            btn.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)
            button.append(btn)
            if name != "Login":
                cursor.execute(f"select username from {txt}")
                pexes = cursor.fetchall()
                pexes = [item[0] for item in pexes]
                if name in pexes:
                    btn.config(bg="#B2E6A0")

        button_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        zpet_button_frame = Frame(w)
        zpet_button_frame.pack(side=BOTTOM, pady=10)
        zpet_play = Objekty("Button", master=zpet_button_frame, text="Zpět", bg="#ffafcc", font=font,
                            command=lambda: zpet(main_frame, entry_frame, zpet_button_frame))
        zpet_play.pack()

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        input_e.bind('<KeyRelease>', lambda event: filtr(event, button))
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
            p = [k.widget.get() for k in pex]
            n = namex.widget.get().replace('-', '_')
            cursor.execute(f'CREATE TABLE p_{n}(value TEXT, username NVARCHAR(255), time DATETIME);')
            cursor.execute(f'INSERT INTO main(name) VALUES (?);', (n))
            cursor.execute(f"SELECT pexes_v FROM login WHERE name LIKE ?", (name,))
            cursor.execute('UPDATE login SET pexes_v = ? WHERE name = ?', (cursor.fetchone()[0] + 1, name))
            for i in p:
                cursor.execute(f'INSERT INTO p_{n}(value) VALUES (?);', (i,))

            hotovo = messagebox.showinfo("Vytvořeno",
                                         "Pexeso bylo úspěšně vytvořeno.\nMůžete si ho nyní zahrát v Play!")

            conn.commit()

            zpet_menu(pex, namex, name_entry, btn, zpet)

        def zpet_menu(entries, name_entry, name_l, start_btn, zpet_btn):
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
                          command=lambda: zpet_menu(entries, name_entry, name_l, start_btn, zpet_btn))
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
                password = create_hash(entry[2])
                cursor.execute('INSERT INTO login(name, password, email, pexeso, pexes_v) VALUES (?, ?, ?, ?, ?);',
                               (entry[1].widget.get(), password, entry[0].widget.get(), 0, 0))
                cursor.commit()
                name = entry[1].widget.get()
                log_btn.config(text=name)
                if var.get() == 1:
                    with open("login.txt", "w", encoding='utf-8') as file:
                        file.write(f"{entry[1].widget.get()}")
                show_main(frame, entry)

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
        frame = Objekty("Frame", master=w, width=600, height=400, bg='lightblue', highlightbackground="#ffd6a5", highlightthickness=4)
        frame.pack(ipady=20, ipadx=50)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        for x in range(4):
            l = Objekty("Label", master=frame.widget, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
            l.grid(row=x, column=0, pady=10)
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
        start_btn.grid(row=6, column=1, pady=10)
        zpet_btn = Objekty("Button", master=frame.widget, text="Zpět", bg="#ffafcc", font=("Helvetica", 12, "bold"), width=15,
                          command=lambda: show_main(frame, entry))
        zpet_btn.grid(row=6, column=0, pady=10)

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
                heslo = unhash_password(entry, result)
                if heslo:
                    name = entry[0].widget.get()
                    log_btn.config(text=name)
                    if var.get() == 1:
                        with open("login.txt", "w", encoding='utf-8') as file:
                            file.write(f"{entry[0].widget.get()}")
                    show_main(frame, [])
                else:
                    error = messagebox.showerror("Nelze přihlásit", "Nesprávné heslo!")

        def email(event, entry):
            global name
            name = entry[0].widget.get()
            e_mail(event, frame)


        name = ["nickname:", "password:"]
        entry = []
        frame = Objekty("Frame", master=w, bg='lightblue', width=600, height=400, highlightbackground="#ffd6a5", highlightthickness=4)
        frame.pack(pady=50)
        for x in range(2):
            l = Objekty("Label", master=frame.widget, text=name[x], bg="#f7f3e9", font=("Helvetica", 12, "bold"))
            l.grid(row=x, column=0, pady=20, padx=20, sticky='nsew')
            if name[x] == "password:":
                e = Objekty("Entry", master=frame.widget, font=("Helvetica", 12), show="*")
            else:
                e = Objekty("Entry", master=frame.widget, font=("Helvetica", 12))
            e.grid(row=x, column=1, pady=20, padx=30, sticky='nsew')
            entry.append(e)

        oko = Objekty("Button", master=frame.widget, image=photo, command=lambda: oko1(entry[1], oko))
        oko.photo = photo
        oko.place(x=345, y=90)

        var = IntVar()

        remember = Objekty("Label", master=frame.widget, text="remember me:", bg="#f7f3e9", font=("Helvetica", 12, "bold"))
        remember.grid(row=2, column=0, pady=15)
        remember_ra = Objekty("Checkbutton", master=frame.widget, font=("Helvetica", 12), variable=var, onvalue=1)
        remember_ra.grid(row=2, column=1)

        label = Objekty("Label", master=frame.widget, text="Zapomněl heslo", fg="black", font=font)
        label.grid(row=3, column=1, pady=10, padx=50)

        start_btn = Objekty("Button", master=frame.widget, text="Login", bg="#ffafcc", font=font, width=5,
                           command=lambda: login_second(entry, frame, var))
        start_btn.grid(row=4, column=1)
        zpet_btn = Objekty("Button", master=frame.widget, text="Zpět", bg="#ffafcc", font=font, width=5,
                          command=lambda: show_main(frame, []))
        zpet_btn.grid(row=4, column=0, pady=10)

        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.bind("<Button-1>", lambda event: email(event, entry))
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

        def on_click(event):
            print("Label byl kliknut!")

        def hide_p():
            if hide.get():
                h = 1
            elif not hide.get():
                h = 0

            with open("h.txt", "w") as h_txt:
                h_txt.write(str(h))

        def safe():
            global name
            if name != l.widget.get():
                error = messagebox.askquestion("Warning", "Opravdu chcete změnit heslo?")
                if error:
                    cursor.execute(f'SELECT name FROM login;')
                    nickname = cursor.fetchall()
                    agree = True
                    for x in nickname:
                        if x[0] == l.widget.get():
                            agree = False
                            break
                    if not agree:
                        error = messagebox.showerror("Error", "Nickname už je použit")
                    else:
                        cursor.execute(f"UPDATE login SET name = ? WHERE name = ?;", (l.widget.get(), name))
                        cursor.commit()
                        name = l.widget.get()
                        log_btn.config(text=name)
                        with open("login.txt", "w", encoding='utf-8') as file:
                            file.write(f"{l.widget.get()}")

            show_main(frame, [])

        def odhlasit(event, frame):
            global name
            name = "Login"
            log_btn.config(text=name)
            with open("login.txt", "w") as login:
                login.write("")
            show_main(frame, [])

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
        hide_pex.grid(row=len(words) + 1, column=1, columnspan=2, pady=10, padx=50)

        bind_l = ["Změnit heslo", "Odhlásit se"]
        for b in range(2):
            label = Objekty("Label", master=frame.widget, text=bind_l[b], fg="black", font=font)
            label.grid(row=len(words)+2, column=b+1, pady=10, padx=50)
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            if b == 0:
                label.bind("<Button-1>", lambda event: change_password(event, frame))
            else:
                label.bind("<Button-1>", lambda event: odhlasit(event, frame))


        zpet_btn = Objekty("Button", master=frame.widget, text="Zpět", bg="#ffafcc", font=font, width=5, command=lambda: show_main(frame, []))
        zpet_btn.grid(row=len(words)+3, column=1, pady=10, padx=10)
        uloz_btn = Objekty("Button", master=frame.widget, text="Uložit", bg="#ffafcc", font=font, width=5, command=safe)
        uloz_btn.grid(row=len(words) + 3, column=2, pady=10, padx=10)
def admin():
    if name == "admin":
        for key in keys.keys():
            w.unbind(f"<KeyPress-{key}>")
            w.unbind(f"<KeyRelease-{key}>")

        sql = 0
        image = "nastavení.ico"

        def command(event):
            nonlocal sql
            list_box_left.insert(END, input_e.get())
            if input_e.get().upper() == "QUIT":
                admin_w.destroy()
            elif sql == 1:
                if input_e.get().upper() == "END":
                    sql = 0
                    list_box_right.insert(END, "Odpojeno od databáze")
                elif input_e.get().upper() == "TABLES":
                    sql_root = Toplevel()
                    sql_root.iconbitmap(image)
                    cursor.execute("select * from sys.tables;")
                    tables = cursor.fetchall()
                    tables = [table[0] + "\n" for table in tables]
                    Label(sql_root, text=tables).pack()
                else:
                    try:
                        cursor.execute(input_e.get())
                        tables = cursor.fetchall()
                        tables = [str(table) + "\n" for table in tables]
                        sql_root = Toplevel()
                        sql_root.iconbitmap(image)
                        Label(sql_root, text=tables).pack()

                    except Exception as e:
                        error = messagebox.showerror("Error", e)
                input_e.delete(0, END)
            elif input_e.get().upper() == "SQL":
                list_box_right.insert(END, "Připojeno k databázi")
                sql = 1
                input_e.delete(0, END)
                for key in keys.keys():
                    w.bind(f"<KeyPress-{key}>", lambda event: update_key_state(event, True))
                    w.bind(f"<KeyRelease-{key}>", lambda event: update_key_state(event, False))
            else:
                input_e.delete(0, END)

        admin_w = Toplevel()
        admin_w.config(bg="black")
        admin_w.geometry("1380x727")
        admin_w.iconbitmap(image)

        top_frame = Frame(admin_w, bg="black")
        bottom_frame = Frame(admin_w, bg="black")
        top_frame.pack(side="top", fill=BOTH, expand=True)
        bottom_frame.pack(side="bottom", fill=X)
        left_frame = Frame(top_frame, bg="black")
        right_frame = Frame(top_frame, bg="black")
        left_frame.pack(side="left", fill=BOTH, expand=True)
        right_frame.pack(side="right", fill=BOTH, expand=True)

        list_box_left = Listbox(left_frame, bg="black", fg="white", font=("Italy", 20), justify="left")
        list_box_left.pack(fill=BOTH, expand=True)

        list_box_right = Listbox(right_frame, bg="black", fg="white", font=("Italy", 20), justify="right")
        list_box_right.pack(fill=BOTH, expand=True)

        input_e = Entry(bottom_frame, font=("Italy", 20))
        input_e.pack(fill=X)

        admin_w.bind("<Return>", command)

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
        'PWD=********;'
    )
    cursor = conn.cursor()
    databaze = True
except Exception:
    databaze = False

w.mainloop()
