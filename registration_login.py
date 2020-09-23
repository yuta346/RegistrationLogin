import tkinter as tk
import tkinter.messagebox as tkm
import sqlite3
import bcrypt

conn = sqlite3.connect('userdata.db')

c = conn.cursor()     #create a cursor

c.execute("""CREATE TABLE IF NOT EXISTS user(
        username text,
        email text,
        password text
    )""")

#create registration window
def register():

    register_screen = tk.Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("300x300")

    topMessage=tk.Label(register_screen, text="Create an Account", bg="#1E90FF",fg="white", width="300", height="2", font=("Calibri", 13)).pack() 
    spacing=tk.Label(register_screen,text="").pack() 

    label1 = tk.Label(register_screen ,text = "Username:")
    label1.pack()
    global Username
    Username = tk.Entry(register_screen)
    Username.pack()


    label2 = tk.Label(register_screen ,text = "Email:")
    label2.pack()
    global register_Email
    register_Email = tk.Entry(register_screen)
    register_Email.pack()


    label3 = tk.Label(register_screen ,text = "Password:")
    label3.pack()
    global register_Password
    register_Password = tk.Entry(register_screen, text="Password:", show="*")
    register_Password.pack()

    spacing=tk.Label(register_screen,text="").pack() 

    Register = tk.Button(register_screen, text="Register", width=21, command=register_user)
    Register.pack()


def register_user():
    c.execute("""SELECT * FROM user""")
    userdata = c.fetchall()
    for user in userdata:
        if user[1] == register_Email.get():
            tkm.showinfo('info', 'Account already exists. Please log in.')
            return
             
    tkm.showinfo('info', "Registration Successful")
    password = register_Password.get()
    hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #hash and salt the password 
    with conn:
        c.execute("INSERT INTO user VALUES (:username, :email, :password)", {'username':Username.get(), 'email':register_Email.get(), 'password':hashAndSalt})

    register_Email.delete(0, tk.END)
    register_Password.delete(0, tk.END)
    Username.delete(0, tk.END)


#registration window
def login():
    login_screen = tk.Toplevel(root)
    login_screen.title("Login")
    login_screen.geometry("300x300")

    topMessage=tk.Label(login_screen, text="Welcome Back!", bg="#1E90FF",fg="white", width="300", height="2", font=("Calibri", 13)).pack() 
    spacing=tk.Label(login_screen, text="").pack() 

    label2 = tk.Label(login_screen ,text = "Email:")
    label2.pack()
    global login_Email
    login_Email = tk.Entry(login_screen)
    login_Email.pack()


    label3 = tk.Label(login_screen ,text = "Password:")
    label3.pack()
    global login_Password
    login_Password = tk.Entry(login_screen, text="Password:", show="*")
    login_Password.pack()

    spacing=tk.Label(login_screen, text="").pack() 

    Login = tk.Button(login_screen, text="Login", width=21, command=login_user)
    Login.pack()


def login_user():

    c.execute("SELECT * FROM user")
    userdata = c.fetchall()
    print(userdata)
    userDict= dict()

    #convert list of tuple to dictionary 
    for user in userdata:
        userDict["Username"]=user[0]
        userDict["Email"] = user[1]
        userDict["Password"]= user[2]

    #check the validity
    for user in userDict:
        if bcrypt.checkpw(login_Password.get().encode(), userDict["Password"]) and userDict["Email"]==login_Email.get():
             tkm.showinfo('User info', "Logged in. Welcome back " + userDict["Username"] +" !")
             login_Email.delete(0, tk.END)
             login_Password.delete(0, tk.END)
             return
    tkm.showinfo('User info', "Login failed, Please register or try again")
    login_Email.delete(0, tk.END)
    login_Password.delete(0, tk.END)

    
def main_window():
    global root
    root = tk.Tk()
    root.title("Registration")
    root.geometry('280x150')

    topMessage=tk.Label(root, text="Choose Login or Register", bg="#1E90FF",fg="white", width="300", height="2", font=("Calibri", 13)).pack() 
    spacing=tk.Label(root, text="").pack() 

    Register = tk.Button(root, text="Register", width=21, command=register)
    Register.pack()

    Login = tk.Button(root, text="Login", width=21, command=login)
    Login.pack()

    root.mainloop()

main_window()