from  tkinter import *
import requests
import hashlib
import sys

def request_api_data(query_char):  # called in check_pass function
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def times_leaked(all_hashes, hash_to_check):  # called in check_pass function
    all_hashes = (line.split(':') for line in all_hashes.text.splitlines())
    for h, count in all_hashes:
        if h == hash_to_check:
            return count  # checks if any of the hash matches the tail has to check
    return 0


def check_pass(password):
    hashed_password = (hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    first5_chars, tail = hashed_password[:5], hashed_password[5:]
    response = request_api_data(first5_chars)  # get all hashes that match first 5 characters
    return times_leaked(response, tail)  # to check which hash matches the tail and how many times pwned

def send():
    hck = int
    var = StringVar
    password = input_pass_entry.get()
    if len(password)>=8:
        count = check_pass(password)
        if (count !=0):
            var = (f"This password was pwned {count} times, and you should probably change your password" )
            ans = Label(app, text=var, width="150", height="3", bg="red",fg="black",font=("calibiri","12"))
            ans.place(y="250")
        else:
            var = (f"Great! This password not pwned yet")
            ans = Label(app, text=var, width="150", height="3", bg="lawn green",fg="black",font=("calibiri","12"))
            ans.place(y="250")
    else:
        var = (f"Please enter a valid password")
        ans = Label(app, text=var, width="150", height="3", bg="red",fg="black",font=("calibiri","12"))
        ans.place(y="250")


app = Tk()
app.geometry("1200x500")
app.title("Password checker")

heading = Label(text="Password Checker",bg="grey", font=("bold", "40"))
heading.place(x="300",y="20")

input_pass = Label(text="Enter your password:",font=("bold", "20"))
input_pass.place(x="220", y="150")

input_pass = StringVar()
input_pass_entry = Entry(textvariable="inut_pass",width="30",show='*')
input_pass_entry.place(x="500", y="150",height="35", width="300")

btn = Button(app, text = "Pwned ?", width="20",font="bold",bg="light blue" ,height="2", command=send)
btn.place(x="450", y="320")

def close_app(): 
    app.destroy()

button = Button (app, text = "Exit", width="20",bg="light blue", command = close_app)
button.place(x="700", y="320",height="50")


mainloop()
