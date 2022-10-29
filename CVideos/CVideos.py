import cv2
import os
import youtube_dl
import sys

videos = [
    # {
    #     "link": "https://www.youtube.com/watch?v=CI7Dxbt_ayk",
    #     "filename": "sentry_bright"
    # },
    {
        "link": "https://github.com/uw-advanced-robotics/aruw-vision-platform-2019/raw/master/.github/sentinel_practice-opt.gif",
        "filename": "sentry_practice"
    },
    {
        "link": "https://github.com/uw-advanced-robotics/aruw-vision-platform-2019/raw/master/.github/ohio23-opt.gif",
        "filename": "competition_gif1"
    },
    {
        "link": "https://github.com/uw-advanced-robotics/aruw-vision-platform-2019/raw/master/.github/ohio48-opt.gif",
        "filename": "competition_gif2"
    },
    # {
    #     "link": "link to video",
    #     "filename": "file name to save video to"
    # }
]
folder = "CVideos"

def download(video):
    print("Downloading "+video.get("filename")+" from "+video.get("link")+" ... ", end="")
    save_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")  # supressing print
    ydl_opts = {
        "outtmpl": folder+"/"+video.get("filename")+".%(ext)s"
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video.get("link")])
    sys.stdout = save_stdout # enabling print
    print("finished")

def downloadAll(refreshAll=False):
    def file_exists(filename):
        for file in os.listdir(folder):
            if os.path.splitext(file)[0] == filename:
                return True
        return False
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for video in videos:
        if not file_exists(video.get("filename")):
            download(video)

def imagefeed(cvfunction):
    print("here for now")

def videofeed(cvfunction, file=None):
    play = False

    def feedfile(filename):
        nonlocal play

        video = cv2.VideoCapture(folder+"/"+filename)
    
        while True:
            success,frame = video.read()
            if success:
                image = cvfunction(frame)
                cv2.imshow("Image", image)
            else:
                return
            key = cv2.waitKey(60 if play else 0)
            if key == ord(' '):
                play = not play

    if not file:
        for filename in os.listdir(folder):
            feedfile(filename)
    else:
        feedfile(file)


downloadAll()