import tkinter as tk
import csv
import pyperclip
import random

radiobuttons = []   # List to keep track of radiobuttons and buttons
buttons = []
username_password_map = {}


#generate password
def shuffle(password):
    tempList=list(password)
    random.shuffle(tempList)
    return ''.join(tempList)

def generate_new_password():

    uppercaseLetter1=chr(random.randint(65,90))
    uppercaseLetter2=chr(random.randint(65,90))
    lowercaseLetter1=chr(random.randint(97,122))
    lowercaseLetter2=chr(random.randint(97,122))
    digit1=chr(random.randint(65,90))
    digit2=chr(random.randint(65,90))
    sign1=chr(random.randint(65,90))
    sign2=chr(random.randint(65,90))

    password=uppercaseLetter1+uppercaseLetter2+lowercaseLetter1+lowercaseLetter2+digit1+digit2+sign1+sign2
    return shuffle(password)


def select_radiobutton(option):
    selection_label.config(text="Selected option: " + option)


def copy_password(username):
    if username in username_password_map:
        password = username_password_map[username]
        
        pyperclip.copy(password)
        
        status_label.config(text=f"Password for {username} copied to clipboard.")
    else:
        status_label.config(text=f"No password found for {username}.")

def add_radio_buttons(column_data, email_data, pass_data):
    for item, item2, item3 in zip(column_data, email_data, pass_data):
        radiobutton = tk.Radiobutton(root, text=item, variable=selected_option, value=item)
        radiobutton.pack(anchor=tk.W)
        radiobuttons.append(radiobutton)
        tk.Label(root, text=item2).pack(anchor=tk.W)
        username_password_map[item] = item3
      
        button = tk.Button(root, text="Copy Password", command=lambda u=item: copy_password(u))
        button.pack(anchor=tk.W)
        buttons.append(button)

def read_csv_file(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        columns = next(reader)
        columns = [col.strip('\ufeff') for col in columns]
        data = {column: [] for column in columns}
        for row in reader:
            for col_index, value in enumerate(row):
                data[columns[col_index]].append(value)
    return data

def add_radiobutton():
    new_option = new_option_entry.get()
    new_mail = new_option_entry_email.get()
    new_password = generate_new_password()

    if new_option:
        
        add_values_to_csv(new_option, new_mail, new_password)
        
        
        radiobutton = tk.Radiobutton(root, text=new_option, variable=selected_option, value=new_option)
        radiobutton.pack(anchor=tk.W)
        radiobuttons.append(radiobutton)
        
        tk.Label(root, text=new_mail).pack(anchor=tk.W)
        
        button = tk.Button(root, text="Copy Password", command=lambda u=new_option: copy_password(u))
        button.pack(anchor=tk.W)
        buttons.append(button)

        username_password_map[new_option] = new_password

       
        new_option_entry.delete(0, tk.END)
        new_option_entry_email.delete(0, tk.END)


def add_values_to_csv(value1,value2,value3):
    with open('data.csv','a',newline='') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow([value1 ,value2,value3])

csv_filename = 'data.csv'
data = read_csv_file(csv_filename)
desired_column = 'App'
column_data = data[desired_column]
username_column = 'Username'
col_data = data[username_column]
pass_column = 'Pass'
pass_data = data[pass_column]


root = tk.Tk()
root.title("Dynamically Add Radiobuttons with Buttons")


selected_option = tk.StringVar()
add_radio_buttons(column_data, col_data, pass_data)


new_option_entry = tk.Entry(root)
new_option_entry.pack()
new_option_entry_email = tk.Entry(root)
new_option_entry_email.pack()


add_button = tk.Button(root, text="Add Radiobutton", command=add_radiobutton)
add_button.pack(pady=5)


selection_label = tk.Label(root, text="")
selection_label.pack()

status_label = tk.Label(root, text="")
status_label.pack()


root.mainloop()