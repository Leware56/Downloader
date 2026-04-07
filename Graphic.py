from tkinter import *
from tkinter import ttk
from Downloader_graphic import *
from tkinter.messagebox import showerror, showwarning, showinfo
import threading

root = Tk()
root.title("Downloader")
root.geometry("700x600")
root.resizable(False, False)


URL = StringVar()
audio_chek = BooleanVar(value= False)
audio_select = IntVar()
duration = StringVar()

def enter():
    global entry
    global audio
    global combobox
    global URL
    global btn
    global QUALITY
    global DURATION
    global duration
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
    combobox["values"] = QUALITY
    duration.set(DURATION[0])
    print(duration)
    print(URL)

def Quality():
    global combobox
    global CHOOSE
    qual_select = combobox.get()
    CHOOSE.pop(0)
    CHOOSE.insert(0,qual_select)

def btn_download():
    global combobox
    global audio
    global CHOOSE
    global URL
    global percent
    print(URL)
    Quality()
    Audio()
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()



def start_downloading():
    global percent
    showinfo(title="ЗАГРУЗКА НАЧАЛАСЬ", message="Загрузка вашего материала началась, мы предупредим вас когда оно закончится")
    while percent == "100%":
        if percent == "100%":
            finish_downloading()
            continue

def finish_downloading():
    showinfo(title="ЗАГРУЗКА ЗАКОНЧИЛАСЬ", message="Загрузка завершилась")

thread1 = threading.Thread(target= downloading(URL), args=URL)
thread2 = threading.Thread(target= start_downloading(), args=None)

def Audio():
    global audio
    if audio_select.get() == 1:
        CHOOSE.pop(2)
        CHOOSE.insert(2,True)
    else:
        CHOOSE.pop(2)
        CHOOSE.insert(2,False)

    

label = Label(text="Добро пожаловать в Downloader!!!",font= "broadway")#Текст
label.place(x=210, y=20)

time = ttk.Label(textvariable= duration) #Время
time.place(x=315, y=450-75-40,)

main_menu = Menu() #Меню
main_menu.add_cascade(label="Настройки")
main_menu.add_cascade(label="Справка")
main_menu.add_cascade(label="О программе")


btn = ttk.Button(text= "Скачать", command=btn_download)#Кнопка скачать
btn.place(x=190,y=400)

btn_find = ttk.Button(text= "Найти", command=enter)#Кнопка "найти"
btn_find.place(x=190+300,y=320-40)

entry = ttk.Entry(textvariable=URL)
entry.place(x=190+97-20,y=320-40, height=30, width= 150)

combobox = ttk.Combobox(values=QUALITY, state="readonly",)#Выбор качества
combobox.place(x=190-80, y=450-75-60, height=50 , width= 80)

audio = ttk.Checkbutton(text="Только звук", variable=audio_select, command=Audio)#Только звук
audio.place(x=315+170, y=450-75-40,)


btn.config(text= "Download",width= 50)
root.config(menu=main_menu)
root.mainloop()