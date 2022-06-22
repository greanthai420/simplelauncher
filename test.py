# LICENSED UNDER AGPLv3
import tkinter as tk
from tkinter import ttk
import subprocess
import string
import tkinter.font as f
from tkinter import messagebox

#file paths
currentaccount_path = 'polymc/currentaccount'
accountsjson_path = 'polymc/accounts.json'
polymcexe_path = 'polymc/polymc.exe'
#polymc settings
instancename = 'greancraftuniverse'
autojoinserver = False
serverip = '127.0.0.1'

#setting up windows
root = tk.Tk()
root.resizable(False, False)
root.title('greancraft universe')

window_width = 300
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

#get current account name from currentaccount file
with open(currentaccount_path, 'r') as file:
    currentaccountdata = file.read()
    #append "" to currentaccount variable into new var
    currentaccount_full = '"' + currentaccountdata + '"'
    #print(currentaccount_full)

#creating frames
topframe = ttk.Frame(root)
topframe.pack(padx=10, pady=10, fill='x', expand=True)
btmframe = ttk.Frame(root)
btmframe.pack(padx=10, pady=10, fill='x', expand=True)

def validate(P):
    if len(P) < 16:
        return True
    else:
        return False
vcmd = (root.register(validate), '%P')

#name to use text box
nametouse = tk.StringVar()
nametouse_label = ttk.Label(topframe, text="ชื่อที่จะใช้ในเกม :")
nametouse_label.pack(fill='x', expand=True)

nametouse_entry = ttk.Entry(topframe, textvariable=nametouse, validate="key", validatecommand=vcmd)
nametouse_entry.insert(1, currentaccountdata)
nametouse_entry.pack(fill='x', expand=True)
nametouse_entry.focus()

def illegalnamepopup():
    # popup = tk.Toplevel()
    # popup.resizable(False, False)    
    # popup.title("ERROR")
    # popup.geometry(f'{window_width}x{50}+{center_x}+{center_y}')

    # font = f.Font(weight="bold", size=14)
    # popup_label = ttk.Label(popup, text= "ชื่อในเกมต้องเป็นภาษาอังกฤษเท่านั้น", foreground='red')
    # popup_label["font"] = font
    # popup_label.pack()
    messagebox.showerror('ERROR', 'ชื่อในเกมต้องเป็นภาษาอังกฤษเท่านั้น')
    

#what to do when launchgame is pressed
def launchgame():
    illegalname = False
    #checks for 0 character
    if len(nametouse_entry.get())==0:
        illegalname = True
    #checks for special characters
    for char in nametouse_entry.get():
        if char not in string.ascii_letters:
            if char not in string.digits:
                illegalname = True
                break
                
    if illegalname == False:
        #appending "" to nametouse
        nametouse_entry_full = '"' + nametouse_entry.get() + '"'
        #write nametouse to currentaccount
        with open(currentaccount_path, 'w') as file:
            file.write(nametouse_entry.get())
        #write nametouse to accounts.json
        with open(accountsjson_path, 'r') as file:
            filedata = file.read()
            #replace x with y
            filedata = filedata.replace('"name": '+currentaccount_full+',', '"name": '+nametouse_entry_full+',')
            filedata = filedata.replace('"userName": '+currentaccount_full, '"userName": '+nametouse_entry_full)
        with open(accountsjson_path, 'w') as file:
            file.write(filedata)
        #launch minecraft and join server
        #args: polymc.exe -l instancename -s serverip
        if autojoinserver == True:
            subprocess.Popen([polymcexe_path, '-l', instancename, '-s', serverip])
            #quit()
        else:
            subprocess.Popen([polymcexe_path, '-l', instancename])
            #quit()
        root.quit()
    else:
        illegalnamepopup()
    
# launch game button
launch_button = ttk.Button(btmframe,text='เริ่มเกม',command=launchgame)
launch_button.pack(ipadx=50,ipady=5,expand=True)

# exit button
exit_button = ttk.Button(btmframe,text='ออก',command=lambda: root.quit())
exit_button.pack(ipadx=50,ipady=5,expand=True)

# display window (need to be in loop or it shows up then immediately exits)
root.mainloop()