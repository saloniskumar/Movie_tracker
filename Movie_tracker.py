import sys
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import sqlite3
import imdb
from datetime import datetime

class IMDBdataBase:
    """IMDb Movie tracking app with login authentication"""
    def __init__(self):
        self.correct_username = "saloni"
        self.correct_password = "SDU"

        # Login Window
        self.login_window = Tk()
        self.login_window.title("Login")
        self.login_window.geometry('300x150')

        self.username_label = Label(self.login_window, text="Username:")
        self.username_label.pack()

        self.username_entry = Entry(self.login_window)
        self.username_entry.pack()

        self.password_label = Label(self.login_window, text="Password:")
        self.password_label.pack()

        self.password_entry = Entry(self.login_window, show="*")
        self.password_entry.pack()

        self.login_button = Button(self.login_window, text="Login", command=self.login)
        self.login_button.pack()

        # Start the login window loop
        self.login_window.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.correct_username and password == self.correct_password:
            messagebox.showinfo("Login Successful!", "You have successfully logged in.")
            self.setup_main_app_window()
        else:
            messagebox.showerror("Error", "Invalid login.")

    def setup_main_app_window(self):
        # Destroy the login window
        self.login_window.destroy()
        
        # Initialize the main app window
        self.window = Tk()
        self.window.config(pady=20, padx=20, bg='#ffb3c6')
        self.window.resizable(False, False)

        self.combo = ttk.Combobox(self.window, state="readonly",
                                 values=['Already_watched', 'To_watch','Currently_Watching'], font=('Papyrus', 10, 'bold'),
                                 justify=CENTER)
        self.combo.grid(row=7, column=0)
        self.combo.current(0)
        self.ano = datetime.now().year

     
        # Set up second window
        self.new_win = Toplevel(self.window)
        self.new_win.title("Choose a movie")
        self.new_win.resizable(False, False)
        self.new_win.config(pady=20, padx=20, bg='#ffc8dd')
        self.new_win.withdraw()
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_closing)
        # IMDB API
        self.moviesDB = imdb.IMDb()
        # database
        self.conn = sqlite3.connect('IMDB_Films5.db')
        # self.conn = sqlite3.connect('IMDB_Films6.db')
        print("Connection was successful")
        self.c = self.conn.cursor()
        self.c.execute(f"CREATE TABLE if not exists Year{self.ano}_Films(id integer PRIMARY KEY, TITLE text, "
                       "YEAR integer, RATING real, DIRECTOR text, ACTORS text, GENRE text, DESCRIPTION text, DATE_ADDED text)")
        self.conn.commit()
        # Set up Tree style
        self.style = ttk.Style()

        self.style.configure("mystyle.Treeview.Heading", font=('Papyrus', 12, 'bold'))
        self.tree = ttk.Treeview(style="mystyle.Treeview", selectmode=BROWSE)
        # Set up the columns
        self.tree['columns'] = ('TITLE', 'YEAR', 'RATING', 'DIRECTOR', 'ACTORS', 'GENRE', 'DESCRIPTION', 'DATE_ADDED')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('TITLE', width=200, minwidth=200, anchor=CENTER)
        self.tree.column('YEAR', width=80, minwidth=80, anchor=CENTER)
        self.tree.column('RATING', width=82, minwidth=82, anchor=CENTER)
        self.tree.column('DIRECTOR', width=150, minwidth=150, anchor=CENTER)
        self.tree.column('ACTORS', width=250, minwidth=250, anchor=CENTER)
        self.tree.column('GENRE', width=230, minwidth=230, anchor=CENTER)
        self.tree.column('DESCRIPTION', width=350, minwidth=350, anchor=CENTER)
        self.tree.column('DATE_ADDED', width=80, minwidth=80, anchor=CENTER)
       
        # Set up the headings
        self.tree.heading('#0', text='', anchor=CENTER)
        self.tree.heading('TITLE', text='Title', anchor=CENTER)
        self.tree.heading('YEAR', text='Year', anchor=CENTER)
        self.tree.heading('RATING', text='Rating', anchor=CENTER)
        self.tree.heading('DIRECTOR', text='Director', anchor=CENTER)
        self.tree.heading('ACTORS', text='Actors', anchor=CENTER)
        self.tree.heading('GENRE', text='Genre', anchor=CENTER)
        self.tree.heading('DESCRIPTION', text='Description', anchor=CENTER)
        self.tree.heading('DATE_ADDED', text='Date added', anchor=CENTER)
   

        self.scroll = Scrollbar(self.window, orient=VERTICAL)
        self.scroll.grid(row=0, column=1, sticky=NS)
        self.tree.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.tree.yview)
        # Bind for tree double click item
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.bind("<Return>", self.OnDoubleClick)

        self.tree.grid(row=0, column=0)
        self.film_lbl = Label(text="Enter your movie:", font=('Papyrus', 15, 'bold'), bg='#ffb3c6', fg='#FFFFFF')
        self.film_lbl.grid(row=1, column=0, pady=5)
        self.entrance = Entry(width=30, font=('Papyrus', 13, 'bold'), fg='#000000', bg='#ffc8dd')
        self.entrance.grid(row=2, column=0)
        self.entrance.focus()
        self.btn = Button(text="Add", font=('Papyrus', 13, 'bold'), bg='#ffc8dd', width=25, command=self.anadir_peli)
        self.btn.grid(row=3, column=0, pady=8)
        self.del_btn = Button(text="Delete a movie", font=('Papyrus', 13, 'bold'), bg='#ffc8dd', width=25,
                              command=self.borrar_peli)
        self.del_btn.grid(row=4, column=0, pady=8)
        self.listed()
       
        self.listt = Listbox(self.new_win, width=50, height=10, highlightthickness=0, font=('Papyrus', 12, 'bold'),
                        selectmode=SINGLE, bg='#ffb3c6', fg='#F2F5FF', selectbackground='#ffb3c6',
                        selectforeground='#ffc8dd', selectborderwidth=3, activestyle=NONE)
        self.listt.grid(row=1, column=0)
        self.scroll = Scrollbar(self.new_win, orient=VERTICAL)
        self.scroll.grid(row=1, column=3, sticky=NS, rowspan=7)
        self.scroll2 = Scrollbar(self.new_win, orient=HORIZONTAL)
        self.scroll2.grid(row=2, column=0, sticky=EW)
        self.listt.config(yscrollcommand=self.scroll.set, xscrollcommand=self.scroll2.set)
        self.scroll.config(command=self.listt.yview)
        self.scroll2.config(command=self.listt.xview)
        # Bind for ListBox double click item
        self.listt.bind('<Double-Button>', self.double_click)

        self.combo.bind("<<ComboboxSelected>>", self.changecombo)


        self.label = Label(text=f'Choose movies in', bg='#ffb3c6',
                           font=('Papyrus', 12, 'bold'), fg='#FFFFFF')
        self.label.grid(row=6, column=0)
        self.window.title(f"Movies  -> ({len(self.tree.get_children())})")

        self.window.mainloop()
        self.conn.close()
        print("Connection disabled.")

    def changecombo(self, event):
        self.ano = self.combo.get()
        try:
            self.listed()
        except sqlite3.OperationalError:
            self.c.execute(f"CREATE TABLE if not exists Year{self.ano}_Films(id integer PRIMARY KEY, TITLE text, "
                           "YEAR integer, RATING real, DIRECTOR text, ACTORS text, GENRE text, DESCRIPTION text, DATE_ADDED text )")
            self.conn.commit()
        finally:
            self.listed()

        self.window.title(f"Movies {self.ano} -> ({len(self.tree.get_children())})")
        self.label.config(text=f'Choose movies in ', bg='#ffb3c6',
                          font=('Papyrus', 12, 'bold'), fg='#FFFFFF')

    def double_click(self, event):
        """Called when user double clicks element from Database"""
        self.entrance.delete(0, 'end')
        self.new_win.clipboard_clear()
        self.new_win.clipboard_append(self.listt.get(self.listt.curselection()))
        self.entrance.insert(0, self.listt.get(self.listt.curselection()))
        messagebox.showinfo(title="Info", message=self.get_movie_info())


    def on_closing(self):
        """Called when user closes second window"""
        self.new_win.withdraw()

    def listed(self):
        """Fill the TreeView with database fields"""
        self.tree.delete(*self.tree.get_children())
        self.c.execute(f"SELECT TITLE, YEAR, RATING, DIRECTOR, ACTORS, GENRE, DESCRIPTION, DATE_ADDED FROM Year{self.ano}_Films")
        rows = self.c.fetchall()
        for row in rows:
            self.tree.insert("", END, values=row)
        self.conn.commit()

    def OnDoubleClick(self, event):
        """Called when user double clicks element from TreeView"""
        curItem = self.tree.focus()
        item = self.tree.item(curItem)
        self.renew()

        messagebox.showinfo(title=f"{item['values'][0]}", message=f"""
TITLE: {item['values'][0]}\n
YEAR: {item['values'][1]}\n
RATING: {item['values'][2]}\n
DIRECTOR: {item['values'][3]}\n
ACTORS: {item['values'][4]}\n
GENRES: {item['values'][5]}\n
DESCRIPTION: {item['values'][6]}\n
DATE_ADDED: {item['values'][7]}""")


    def renew(self):
        curItem = self.tree.focus()
        item = self.tree.item(curItem)
        self.entrance.delete(0, "end")
        self.entrance.insert(0, item['values'][0])

    def anadir_peli(self):
        """Insert film fields to Database"""
        if self.entrance.get() == "" or self.entrance.get().isspace():
            messagebox.showerror(title="Error", message='THIS MOVIE DOES NOT EXIST')
        else:
            peli = self.entrance.get().strip().lower()
            self.c.execute(f"SELECT TITLE FROM Year{self.ano}_Films")
            rows = self.c.fetchall()
            row = [item[0].lower() for item in rows]
            if peli in row:
                messagebox.showerror(title="Error", message="THIS MOVIE IS ALREADY IN YOUR DATABASE .")
            else:
                try:
                    movies = self.moviesDB.search_movie(peli)
                    id_peli = movies[0].getID()
                    movie = self.moviesDB.get_movie(id_peli)
                    title = movie['title']
                    year = movie['year']
                    rating = movie['rating']
                    directors = movie['directors']
                    casting = movie['cast']
                    sentence = ""
                    for cas in casting[0:5]:
                        sentence += str(f'{cas}, ')
                    genress = movie['genres']
                    genres = ""
                    for gen in genress:
                        genres += str(f'{gen}, ')
                    plot = movie['plot']
                except:
                    messagebox.showerror(title="Error", message="ERROR OCCURED WHILE ADDING THE MOVIE.")

                    
                # Inserting movie into database
                try:
                    self.c.execute(f"""INSERT INTO Year{self.ano}_Films(TITLE, YEAR, RATING, DIRECTOR, ACTORS, GENRE, DESCRIPTION, DATE_ADDED) 
                                            VALUES(?,?,?,?,?,?,?,?);""",
                                           (str(title), int(year),
                                            float(rating), str(directors[0]),
                                            str(sentence),
                                            str(genres), str(plot[0]),
                                            str(datetime.today().strftime('%d/%m/%Y')))),
                    self.listed()
                except UnboundLocalError:
                    pass
            self.label.config(text=f'Choose movies in', bg='#ffb3c6',
                           font=('Papyrus', 12, 'bold'), fg='white')
            self.window.title(f"Movies {self.ano} -> ({len(self.tree.get_children())})")
            self.conn.commit()

    def borrar_peli(self):
        """Delete selected film from database"""

        try:
            curItem = self.tree.focus()
            item = self.tree.item(curItem)
            mb = messagebox.askyesno(title="ATTENTION!", message=f"Are you sure you want to delete this movie: "
                                                                f"{(str(item['values'][0]))}?")
            if mb:
                self.c.execute(f"DELETE FROM Year{self.ano}_Films where TITLE = (?);", (str(item['values'][0]),))
        except IndexError:
            messagebox.showinfo(title='Info', message='PLEASE SELECT A MOVIE')
            print("Index Error")
        self.conn.commit()
        self.listed()
        self.label.config(text=f'Choose movies in', bg='#ffb3c6',
                          font=('Papyrus', 12, 'bold'), fg='white')
        self.window.title(f"Movies {self.ano} -> ({len(self.tree.get_children())})")

    def get_movie_info(self):
        """Get selected movie info when users double click it"""
        peli = self.listt.get(self.listt.curselection())

        movies = self.moviesDB.search_movie(peli)
        id_peli = movies[0].getID()
        movie = self.moviesDB.get_movie(id_peli)
        title = movie['title']
        year = movie['year']
        rating = movie['rating']
        directors = movie['directors']
        casting = movie['cast']
        plot = movie['plot']
        sentence = ""
        for cas in casting[0:5]:
            sentence += str(f'{cas}, ')
        genress = movie['genres']
        genres = ""
        for gen in genress:
            genres += str(f'{gen}, ')
        info = f"""
TITLE: {title}\n
YEAR: {year}\n
RATING: {rating}\n
DIRECTOR: {directors[0]}\n
ACTORS: {sentence}\n
GENRE: {genres}\n
DESCRIPTION: {plot[0]}"""
        return info

        self.window.mainloop()

# Only run the app if this file is executed as a script (not imported as a module)
if __name__ == "__main__":
    imdb = IMDBdataBase()