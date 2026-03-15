import yt_dlp
import json
import subprocess

LOGFILLE = "log.json"
choose = []*3 #1.Качество 2.Промежуток 3.Скачать только звук
quality = []*8
audio = True
duration = 0
INFO = ""
def info_url(URL): # Парсим всё данные, которые он может предоставить (для граф. приложения)
    index_dur = 0
    global INFO
    global quality
    global audio
    global duration
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(URL, download=False)
        INFO = json.dumps(ydl.sanitize_info(info))
        if INFO.find("\"height\": 144") != -1:
            quality.insert(0,"144")
        if INFO.find("\"height\": 240") != -1:
            quality.insert(1,"240")
        if INFO.find("\"height\": 360") != -1:
            quality.insert(2,"360")
        if INFO.find("\"height\": 480") != -1:
            quality.insert(3,"480")
        if INFO.find("\"height\": 720") != -1:
            quality.insert(4,"720")
        if INFO.find("\"height\": 1080") != -1:
            quality.insert(5,"1080")
        if INFO.find("\"height\": 1440") != -1:
            quality.insert("1440")
        if INFO.find("\"height\": 2160") != -1:
            quality.insert(7,"2160")
        index_dur = INFO.find("duration_string")
        print(index_dur)
        duration = INFO[index_dur + 19: INFO.find("\"",index_dur + 19)]# Поиск с начала первой кавычки до конца второй кавычки через поиска её индекса
        print(duration)
        print(quality)
        if INFO.find("audio only") != -1:
            audio = audio
        else:
            audio = False
        print(audio)
    with open(LOGFILLE,"w+") as file:
        file.write(INFO)
        print("Инофрмация была записана")

def Download():   # Загрузка видео или звука

    # Выбираем индекс качества
    global choose
    print(f'''Выберите качество 1-{len(quality)} 
          {quality}''')
    choose.append(quality[int(input(">> "))-1])

    print(f'''Выберите промежуток видео который вы хотите скачать (по умолчанию всё видео) 
          Используйте \"-\", чтобы выбрать промежуток от и до
          Время вашего видео {duration}''')
    temp_dur = input(">> ")
    if temp_dur != "": # Промежуток
        choose.append(temp_dur)
    else:
        choose.append(f"0-{duration}")

        #Звук
    temp_audio = ""   
    print('''Скачать только звук (Y= \"да\", N= \"нет\")
         Y/N(default = N)''')
    temp_audio = str(input(">> ")) 
    if temp_audio.startswith("Y") == True or temp_audio.startswith("y") == True:
        choose.append(True)
    else:
        choose.append(False)
    print(choose)

    def downloading(): # процесс загрузки
        global URL
        if choose[2] == True: #если выбранно только аудио
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
                'format' : F"bv*[height<={choose[0]}]+ba/b[height<={choose[0]}]",
                }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(URL)
    downloading()

def main():
    global URL
    URL= str(input("Введите ссылку >> "))
    info_url(URL)
    Download()
main()
