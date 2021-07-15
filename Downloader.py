from selenium import webdriver
import time
import youtube_dl
import os
from youtube_dl import DownloadError

count = 0
if os.stat("counter.txt").st_size != 0:
    with open("counter.txt") as file:
        count = int(file.read())
    with open("counter.txt", "w") as file:
        file.write(str(count + 1))
else:
    with open("counter.txt", "w") as file:
        file.write("100")
        count = 100

url = input("Enter link of a playlist or video: ")
if "playlist" in url:
    driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
    driver.get(url)
    time.sleep(2)

    playlist = []
    videos = driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')

    for video in videos:
        link = video.find_element_by_xpath('.//*[@id="content"]/a').get_attribute("href")
        playlist.append(link)
    driver.quit()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'Playlist/%(title)s.%(ext)s',
        'noplaylist': True,
        'ignore-errors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    for url in playlist:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except youtube_dl.utils.DownloadError:
            continue
        except youtube_dl.utils.ExtractorError:
            continue
else:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'Music-list-{count + 1}/%(title)s.%(ext)s',
        'noplaylist': False,
        'ignore-errors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
