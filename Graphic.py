from tkinter import *
from tkinter import ttk
from Downloader_graphic import *

root = Tk()
root.title("Downloader")
root.geometry("700x600")
root.resizable(False, False)


URL = StringVar()
audio_chek = BooleanVar(value= False)
DURATION = IntVar()
audio_select = IntVar()
DURATION = StringVar()

def enter():
    global entry
    global audio
    global combobox
    global URL
    global btn
    global QUALITY
    global DURATION
    QUALITY.clear()
    URL = entry.get()
    if len(URL) <= 40:
        btn["state"] = ["disabled"]
        combobox["state"] = ["disabled"]
        audio["state"] = ["disabled"]
        print(len(URL))
    else:
        btn["state"] = ["normal"]
        combobox["state"] = ["readonly"]
        audio["state"] = ["normal"]
        info_url(URL)
    time["textvariable"] = DURATION
    combobox["values"] = QUALITY
    print(DURATION)

def Quality():
    global combobox
    global CHOOSE
    qual_select = combobox.get()
    CHOOSE.append(qual_select)

def Audio():
    global audio
    if audio_select.get() == 1:
        CHOOSE.insert(2,True)
    else:
        CHOOSE.insert(2,False)

    

label = Label(text="Добро пожаловать в Downloader!!!",font= "broadway")#Текст
label.place(x=210, y=20)

time = ttk.Label(textvariable= DURATION) #Время
time.place(x=315, y=450-75-40,)

main_menu = Menu() #Меню
main_menu.add_cascade(label="Настройки")
main_menu.add_cascade(label="Справка")
main_menu.add_cascade(label="О программе")


btn = ttk.Button(text= "Скачать")#Кнопка скачать
btn.place(x=190,y=400)

btn_find = ttk.Button(text= "Найти", command=enter)#Кнопка "найти"
btn_find.place(x=190+300,y=320-40)

entry = ttk.Entry(textvariable=URL)
entry.place(x=190+97-20,y=320-40, height=30, width= 150)

combobox = ttk.Combobox(values=QUALITY, state="readonly")#Выбор качества
combobox.place(x=190-80, y=450-75-60, height=50 , width= 80)

audio = ttk.Checkbutton(text="Только звук", variable=audio_select, command=Audio)#Только звук
audio.place(x=315+170, y=450-75-40,)


btn.config(text= "Download",width= 50)
root.config(menu=main_menu)
root.mainloop()
