import yt_dlp
import json
import subprocess

LOGFILLE = "log.json"
CHOOSE = []*3 #1.Качество 2.Промежуток 3.Скачать только звук
QUALITY = []*8
audio = True
DURATION = 0
INFO = ""
URL = ""
def info_url(URL): # Парсим всё данные, которые он может предоставить (для граф. приложения)
    index_dur = 0
    global INFO
    global QUALITY
    global audio
    global DURATION
    with yt_dlp.YoutubeDL() as ydl:
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
            QUALITY.insert("1440")
        if INFO.find("\"height\": 2160") != -1:
            QUALITY.insert(7,"2160")
        index_dur = INFO.find("duration_string")
        DURATION = INFO[index_dur + 19: INFO.find("\"",index_dur + 19)]# Поиск с начала первой кавычки до конца второй кавычки через поиска её индекса
        print(QUALITY)
        print(DURATION)



def Duration():
    global CHOOSE
    print(f'''Выберите промежуток видео который вы хотите скачать (по умолчанию всё видео) 
          Используйте \"-\", чтобы выбрать промежуток от и до
          Время вашего видео {DURATION}''')
    temp_dur = input(">> ")
    if temp_dur != "": # Промежуток
        CHOOSE.append(temp_dur)
    else:
        CHOOSE.append(f"0-{DURATION}")

def Audio():
        #Звук
    global CHOOSE
    temp_audio = ""   
    print('''Скачать только звук (Y= \"да\", N= \"нет\")
         Y/N(default = N)''')
    temp_audio = str(input(">> ")) 
    if temp_audio.startswith("Y") == True or temp_audio.startswith("y") == True:
        CHOOSE.append(True)
    else:
        CHOOSE.append(False)
    print(CHOOSE)


def downloading(): # процесс загрузки
    global URL
    global CHOOSE
    if CHOOSE[2] == True: #если выбранно только аудио
        only_sound = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }
        with yt_dlp.YoutubeDL(only_sound) as ydl:
            error_code = ydl.download(URL)
    else:

        ydl_opts = {
            'format' : F"bv*[height<={CHOOSE[0]}]+ba/b[height<={CHOOSE[0]}]",
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(URL)

def entery():
    info_url(URL)