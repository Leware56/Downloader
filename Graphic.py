from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
import threading
import yt_dlp
import json
import webbrowser
import os

PATH = ""
Setings_file = "cfg.txt"
if os.path.isfile(Setings_file) == True:
    with open(Setings_file, "r") as file:
        PATH = file.readline()
        file.close()
else:
    with open(Setings_file, "w+") as file:
        file.write("CURRENT")
        PATH = "CURRENT"
        file.close()


CHOOSE = [None]*2 #1.Качество 2.Скачать только звук
QUALITY = []*8
INFO = ""
URL = [""]
DURATION = [""]

def info_url(URL): # Парсим всё данные, которые он может предоставить (для граф. приложения)
    index_dur = 0
    global INFO
    global QUALITY
    global audio
    global DURATION
    ydl_opts = {
        'nocheckcertificate': True,   # отключает проверку SSL
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        INFO = json.dumps(ydl.sanitize_info(info))
        if INFO.find("\"height\": 144") != -1:
            QUALITY.insert(0,"144")
        if INFO.find("\"height\": 240") != -1:
            QUALITY.insert(1,"240")
        if INFO.find("\"height\": 360") != -1:
            QUALITY.insert(2,"360")
        if INFO.find("\"height\": 480") != -1:
            QUALITY.insert(3,"480")
        if INFO.find("\"height\": 720") != -1:
            QUALITY.insert(4,"720")
        if INFO.find("\"height\": 1080") != -1:
            QUALITY.insert(5,"1080")
        if INFO.find("\"height\": 1440") != -1:
            QUALITY.insert(6,"1440")
        if INFO.find("\"height\": 2160") != -1:
            QUALITY.insert(7,"2160")
        index_dur = INFO.find("duration_string")
        DURATION[0] = INFO[index_dur + 19: INFO.find("\"",index_dur + 19)]# Поиск с начала первой кавычки до конца второй кавычки через поиска её индекса

def progress_hook(d):
        global progerssbar
        global Percent
        if d['status'] == 'downloading':
            # Вычисляем процент загрузки
            p = d.get('_percent_str', '0%').replace('%','')
            progerssbar['value'] = float(p)
            Percent = str(p)
            root.update_idletasks() # Обновляем GUI




root = Tk()
root.title("Downloader")
root.geometry("700x600")
root.resizable(False, False)


URL = StringVar()
audio_chek = BooleanVar(value= False)
audio_select = IntVar()
duration = StringVar()
Percent = StringVar()

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
    print(URL)
    Quality()
    Audio()
    start_downloading()



def start_downloading():
    global Percent
    global progerssbar
    global CHOOSE
    global URL
    def progerss_bar():
        global progerssbar
        global Percent
        global CHOOSE
        global URL
        window = Toplevel()
        window.resizable(False, False)
        window.title("Загрузка...")
        window.geometry("250x100")
        progerssbar=ttk.Progressbar(window,orient="horizontal", length=150)
        progerssbar.pack(anchor=CENTER, pady=20)
        Percent_label = ttk.Label(window,textvariable=Percent)
        Percent_label.place(x= 100, y= 100)
        def progress_hook(d):
            global progerssbar
            global Percent
            if d['status'] == 'downloading':
                # Вычисляем процент загрузки
                p = d.get('_percent_str', '0%').replace('%','')
                progerssbar['value'] = float(p)
                Percent = str(p)
                root.update_idletasks() # Обновляем GUI

        def downloading(URL): # процесс загрузки
            global CHOOSE
            if CHOOSE[1] == True: #если выбранно только аудио
                if PATH == 'CURRENT':
                    only_sound = {
                        'format': 'm4a/bestaudio/best',
                        'progress_hooks': [progress_hook],
                        'nocheckcertificate': True,   # отключает проверку SSL
                        'outtmpl': '%(title)s.%(ext)s',
                        'no_color': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'm4a',
                        }]
                    }
                    with yt_dlp.YoutubeDL(only_sound) as ydl:
                        error_code = ydl.download(URL)
                else:
                    only_sound = {
                        'format': 'm4a/bestaudio/best',
                        'progress_hooks': [progress_hook],
                        'nocheckcertificate': True,   # отключает проверку SSL
                        'outtmpl': f'{PATH}\%(title)s.%(ext)s',
                        'no_color': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'm4a',
                        }]
                    }
                    with yt_dlp.YoutubeDL(only_sound) as ydl:
                        error_code = ydl.download(URL)
            else:
                if PATH == 'CURRENT':
                    ydl_opts = {
                        'format' : F"bv*[height<={CHOOSE[0]}]+ba/b[height<={CHOOSE[0]}]",
                        'nocheckcertificate': True,   # отключает проверку SSL
                        'outtmpl': '%(title)s.%(ext)s',
                        'progress_hooks': [progress_hook],
                        'no_color' : True,
                        }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        error_code = ydl.download(URL)
                else:
                    ydl_opts = {
                        'format' : F"bv*[height<={CHOOSE[0]}]+ba/b[height<={CHOOSE[0]}]",
                        'nocheckcertificate': True,   # отключает проверку SSL
                        'outtmpl': f'{PATH}\%(title)s.%(ext)s',
                        'progress_hooks': [progress_hook],
                        'no_color' : True,
                        }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        error_code = ydl.download(URL)
                
        threading.Thread(target=downloading, args = (URL,)).start()
    threading.Thread(target=progerss_bar).start()


def Setings():
    global PATH
    SetWin = Toplevel()
    SetWin.geometry('550x270')
    SetWin.resizable(False,False)
    SetWin.title("Настройки")
    Path_label = ttk.Label(SetWin,text="Путь сохранения файлов")
    Path_label.place(x= 185, y= 38)
    Choose_path = StringVar(SetWin,value = "disabled")

    def disable_choose():
        if Choose_path.get() == "disabled":
            CB_path_user_entry["state"] = ["disabled"]
        else:
            CB_path_user_entry["state"] = ["normal"]



    CB_path = ttk.Radiobutton(SetWin,text="Сохранять в папке, в которой находится эта программа", value= "disabled", variable=Choose_path, command= disable_choose)
    CB_path_user = ttk.Radiobutton(SetWin,text="Пользовательский путь", value= "enabled", variable=Choose_path, command= disable_choose)

    CB_path.place(x= 43, y= 116-20)
    CB_path_user.place(x= 43, y= 192-20-30)

    CB_path_user_entry = ttk.Entry(SetWin,textvariable=PATH)
    CB_path_user_entry.place(x=55 ,y= 220-20-30)

    def Change_path():
        global PATH
        if Choose_path.get() == "disabled":
            PATH = "CURRENT"
            with open(Setings_file, "w+") as file:
                file.write(f"CURRENT")
                file.close()
            showinfo(title="Настройки", message="Настройки изменены")

        else:
            if CB_path_user_entry.get() != "" or " ":
                PATH = CB_path_user_entry.get()
                with open(Setings_file, "w+") as file:
                    file.write(f"{PATH}")
                    file.close()
                showinfo(title="Настройки", message="Настройки изменены")

    SetButton_save = ttk.Button(SetWin ,text= "Сохранить", command= Change_path)
    SetButton_save.place(x= 210, y= 210)

    


def About():
    SetWin = Toplevel()
    SetWin.geometry('550x350')
    SetWin.resizable(False,False)
    SetWin.title("О программе")




def Audio():
    global audio
    if audio_select.get() == 1:
        CHOOSE.pop(1)
        CHOOSE.insert(1,True)
    else:
        CHOOSE.pop(1)
        CHOOSE.insert(1,False)



label = Label(text="Добро пожаловать в Downloader!!!",font= "broadway")#Текст
label.place(x=210, y=20)

dur = ttk.Label(textvariable= duration) #Время
dur.place(x=315, y=450-75-40,)

main_menu = Menu() #Меню
main_menu.add_cascade(label="Настройки", command=Setings)
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
